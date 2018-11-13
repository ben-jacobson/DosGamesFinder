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

from fabric.contrib.files import exists#, append 
from fabric.api import cd, run, local#, env
import json

REPO_URL = 'https://github.com/ben-jacobson/DosGamesFinder.git'  

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
    if exists('.git'):  
        run('git fetch')  
    else:
        run(f'git clone {REPO_URL} {site_folder}')  
    current_commit = local("git log -n 1 --format=%H", capture=True)  
    run(f'git reset --hard {current_commit}')      
    
def _install_project_dependancies():
    run('pip install -r requirements.txt')
    
def _run_database_migration():
    run('python manage.py migrate')
    
def _run_unit_tests():
    run('python manage.py test dosgamesfinder')
    
def initial_config():
    # pull in server_secrets JSON file to set environment variables 
    server_secrets = _read_json_data_fromfile('server_secrets.json')
    print(server_secrets['remote_home_folder'])

    site_folder = server_secrets['remote_home_folder']  
    run(f'mkdir -p {site_folder}')  

    cd(site_folder)
    #run('sudo apt install python3')
    #run('sudo apt install python3-pip')
    #run('sudo apt install git')
    #_install_wsgi()
    _get_latest_source_from_git(site_folder)
    _install_project_dependancies()
    #_run_database_migration()
    #_run_unit_tests()

def deploy():
    pass