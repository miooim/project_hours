# Project hours
Small web app to manage hours invested in various projects by different people

Build on tonado with ldap authentication
Uses Mongodb as a backbone database
AngularJS client side
And bootstrap 3.0 for css
Python 2.7 (Should be also working on 3.0 but not tested)
Tested on Crome (should be working with IE 10 and Firefox)

Built on MAT (Mongo, Angular, Tornado) fraimwork developed by David Levi

# Install
pull from git.
bower install - from web_res directory
pip install -r requirements from project root, I would suggest using virtual environment

# Configuration
Configuration uses tornado options - see config.py in src directory to configure databases, ports etc...

# Run
python app.py

# To do
Authentication groups
Better analysis
Quick dashboard for analysis
Tests
Better documentation and docstrings
