[![Build Status](https://travis-ci.org/okellogabrielinnocent/MyDiary.svg?branch=master)](https://travis-ci.org/okellogabrielinnocent/MyDiary?branch=develop)
[![Coverage Status](https://coveralls.io/repos/github/okellogabrielinnocent/MyDiary/badge.svg?branch=challenge3)](https://coveralls.io/github/okellogabrielinnocent/MyDiary?branch=challenge3)
[![Maintenance](https://img.shields.io/maintenance/yes/2018.svg)](https://codeclimate.com/github/okellogabrielinnocent/MyDiary)
[![Maintainability](https://api.codeclimate.com/v1/badges/ac11ed19fceb907af12a/maintainability)](https://codeclimate.com/github/okellogabrielinnocent/MyDiary/maintainability)
[![GitHub issues](https://img.shields.io/github/issues/okellogabrielinnocent/MyDiary.svg)](https://github.com/okellogabrielinnocent/MyDiary/issues)



# MyDiary
 MyDiary is an online journal where users can pen down their thoughts and feelings.

**Features**
1. Users can create an account and log in.
2. Users can view all entries to their diary.
3. Users can view the contents of a diary entry.
4. Users can add or modify an entry.

**API end points**

EndPoint | Functionality
------------ | -------------
POST /api/v1/auth/signup|Creates new user
POST /api/v1/auth/login|Signs in a new user
GET /entries | Fetches all entries
POST /entries|Create an entry
GET /entries/<'entryId>|Fetch a single entry
PUT /entries/<'entryId>|Modify an entry


**Getting Started**

These instructions will enable you to run the project on your local machine.


**Prerequisites**

Below are the things you need to get the project up and running.

- git : To update and clone the repository
- python3: Language used to develop the api
- pip: A python package used to install project requirements specified in the requirements text file.
- PostgresSQL installed and running

 **Set Up database**
 - Download and install postgresSQL
 - Create database and name it mydiary
 
**Installing the project**

Type:        
       "https://github.com/okellogabrielinnocent/MyDiary.git"
  in the terminal or git bash or command prompt.
- Install the virtual enviroment with virtualenv env
- change directory to virtual enviroment with cd env
- change directory to virtual enviroment with cd Scripts
- Type "activate" to activate virtual environment
- Change directory back to folder by typing cd.. (*2)
- Install requirements

To install the requirements. run:

      pip install -r requirements.txt

cd to the folder mydiary
And from the root of the folder, type:
      
      python run.py
      
To run the tests and coverage, from the root folder, type: 
        
      coverage run -m pytest 
      or nose2 -v
      or nosetests -v --with-coverage
      coverage report
