# Project hours
Small web app to manage hours invested in various projects by different people

Build on tornado with ldap authentication
Uses Mongodb as a backbone database
AngularJS client side
And bootstrap 3.0 for css
Python 2.7 (Should be also working on 3.0 but not tested)
Tested on Chrome (should be working with IE 10 and Firefox)

Built on MTA (Mongo, Tornado, Angular) 

framework developed by David Levi: https://github.com/davidvoler/mongodb-tornado-angular.

# Install
pull from git

bower install - from web_res directory

pip install -r requirements from project root, I would suggest using virtual environment

# Configuration
Configuration uses tornado options - see config.py in src directory to configure databases, ports etc...
Don't forget to configure ldap servers and ports...

# Run
python app.py

Go to web page->hamburger menu->admin->Projects and add some projects...
Here you ready to work...

# To do
Authentication groups

Better analysis

Quick dashboard for analysis

Tests

Better documentation and docstrings
