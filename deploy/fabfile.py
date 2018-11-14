''' 

DEPLOY - Script for ongoing automated deployments

INITIAL_CONFIG - Script for initial config of the server, not for regular deployments.

Using Fabric, this script will remotely: 
    - Install Python 3
    - Install Pip3
    - Install Git
    - Install Nginx / Gunicorn
    - Clone the latest release of code into /home/ubuntu/sites/*site_name*
    - Using PIP, install the dependancies
    - Run a database migration
    - Run the unit tests built into the project and output the results for debugging
'''

from fabric.contrib.files import exists, append, sed 
from fabric.api import cd, run, local#, env
import json
import random

REPO_URL = 'https://github.com/ben-jacobson/DosGamesFinder.git'  

def _return_line_number_of_string(filename, string, starting_at=0):
    '''
    Read a file, search for a string, then return the line number
    '''
    with open(filename) as file_handle:
        for num, line in enumerate(file_handle, 1):
            if num >= starting_at and string in line:
                return num

def _read_json_data_fromfile(filename):
    #read_data = []
    with open(file=filename, mode='r') as json_data:
        read_data = json.load(json_data,) 
    return read_data
    
def _install_wsgi():
    run('sudo apt install nginx')
    run('sudo systemctl start nginx')
    run('pip install gunicorn')
    
def _get_latest_source_from_git(site_folder):
    '''
    Used for both initial deployment and ongoing deployment, this will pull down the source from the remote repo and run git reset --hard
    '''
    if exists('.git'):  # check if it's a git repo already. 
        run('git fetch')  
    else:
        run(f'git clone {REPO_URL} .')  

    current_commit = local("git log -n 1 --format=%H", capture=True)  
    run(f'git reset --hard {current_commit}')      
    
def _install_project_dependancies():
    run('pip install -r requirements.txt')
    
def _alter_django_settings_py(site_folder, server_secrets):
    # alter the allowed hosts in settings.py
    settings_file = site_folder + '/restapp/settings.py'
    site_name = server_secrets['site_name']

    sed(settings_file, "DEBUG = True", "DEBUG = False")
    sed(settings_file, 
        'ALLOWED_HOSTS = .+$', 
        f'ALLOWED_HOSTS = ["{site_name}"]'
    )

    # alter the secret key, by creating a secret key file and pointing settings.py to it
    secret_key_file = site_folder + '/restapp/secret_key.py'
    if not exists(secret_key_file):
        chars  = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_file, '\nfrom .secret_key import SECRET_KEY')
        
    # alter the database object - it's too fiddly to replace the existing object, instead we'll append to end of file which should overload
    database_object = f"""
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{server_secrets["dbase_name"]}',
        'USER': '{server_secrets["dbase_user"]}',
        'PASSWORD': '{server_secrets["dbase_pass"]}',
        'HOST': 'localhost',
        'PORT': '{server_secrets["dbase_port"]}',
        'TEST': {{
            'NAME': 'dosgamesfinder_test', 
        }},        
    }}
}}
    """         # the {{ or }} are for  terminating the curly brackets
    #append(settings_file, f'\n\n{database_object}') # found that if string exists in file, append is not run. 
    run(f'echo "\n\n{database_object}" >> {settings_file}')

def _run_database_migration():
    run('python manage.py migrate')
    
def _run_unit_tests():
    run('python manage.py test dosgamesfinder')
    
def initial_config():
    # pull in server_secrets JSON file to set environment variables 
    server_secrets = _read_json_data_fromfile('server_secrets.json')
    site_folder = server_secrets['remote_home_folder']  
    run(f'mkdir -p {site_folder}')  

    with cd(site_folder):
        # todo - install postgresql + config it
        run('sudo apt install python3')        # todo - add in creating symbolic links so that commands can be run just by typing python, not needing to type python3
        run('sudo apt install python3-pip')    # todo - same as above but with pip
        run('sudo apt install git')
        _install_wsgi()
        # todo - add nginx / gunicorn config
        _get_latest_source_from_git(site_folder)
        _install_project_dependancies()
        _alter_django_settings_py(site_folder, server_secrets)
        _run_database_migration()
        _run_unit_tests()

def deploy():
    pass