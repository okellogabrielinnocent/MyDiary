[![Build Status](https://travis-ci.org/okellogabrielinnocent/MyDiary.svg?branch=master)](https://travis-ci.org/okellogabrielinnocent/MyDiary?branch=develop)
[![Coverage Status](https://coveralls.io/repos/github/okellogabrielinnocent/MyDiary/badge.svg?branch=develop)](https://coveralls.io/github/okellogabrielinnocent/MyDiary?)
# MyDiary
 MyDiary is an online journal where users can pen down their thoughts and feelings.

**Features**
1. Users can create an account and log in.
2. Users can view all entries to their diary.
3. Users can view the contents of a diary entry.
4. Users can add or modify an entry.

**API end points**

- GET /api/v1/entries (gets all entries)
- GET /api/v1/entries/<entryId> (get entry by id)
- PUT /api/v1/entries/<entryId> (Updates entry of given id)
- POST /api/v1/entries (Creates new entry with POST method)

**Getting Started**

These instructions will enable you to run the project on your local machine.
Set up postgress
**Prerequisites**

Below are the things you need to get the project up and running.

- git : To update and clone the repository
- python3: Language used to develop the api
- pip: A python package used to install project requirements specified in the requirements text file.

**Installing the project**

Type: 
        
       "https://github.com/okellogabrielinnocent/MyDiary.git"
  in the terminal or git bash or command prompt.

To install the requirements. run:

      pip install -r requirements.txt

cd to the folder ride-my-way
And from the root of the folder, type:
      
      python run.py
      
To run the tests and coverage, from the root folder, type: 
        
        coverage run -m pytest or nose2 -v
        coverage report
