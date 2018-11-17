DosGamesFinder - 2018, Ben Jacobson

This is a small project to test what I've learned with Django, Django REST API, Backbone, jQuery and Bootstrap. The goal is to create fun single page app using all the components you might use for a commercial grade application. 

Site is currently live at http://www.dosgamesfinder.com

Installation instructions - 
- Requires Python 3.6 to be installed on your machine, it is recommended that you create 
  a virtual environment for this. Throughout development I've used VirtualEnv: 
    $ mkvirtualenv --python=python3.6 dosgamesfinder
- In your VirtualEnv, you can run the following command to automatically add all 
  pre-requisite python packages, eg Django, DjangoREST, etc:
    $ pip install -r requirements.txt
- Django has a built in virtual server for local testing, run it with
    $ python manage.py runserver
- If no errors, use your web browser to visit http://localhost:8000

Testing instructions - 
- To run unit tests:
    $ python manage.py test dosgamesfinder
- (Coming Soon) To run functional / integration tests:
    $ python manage.py test functional_tests
- (Coming Soon) QUnit for testing Backbone and Jquery

Deployment instructions - 
- See fabfile.py in deploy/ folder