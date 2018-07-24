from flask import jsonify
import os
import re
from flask import Flask, jsonify, request
from utilities.validations import ValidateInputs

class Entry:
    '''
    lets have lists of entries 
    '''
    entries=[
            {
            'id':'1',
            'tittle':'Gabby',
            'body':'Technical Leader is the best way to learn from your ego and teach others the new technologies ',
            'date':'20-12-2018'
            },
            {
            'id':'2',
            'tittle':'Software Engineer',
            'body':'Living in the world of engineering is cool and better for the revolution of the world',
            'date':'20-12-2018'
            }
            ]


    def __init__(self, id, tittle, body, date):
        
        self.entryId = 0
        self.tittle = None
        self.body = None
        self.date = None

    def check_entry(self, tittle):
        if not isinstance(tittle, str) or tittle == None or tittle == "":
            return False
        check_entry = False
        for entry in self.entries:
            for key in entry:
                if key == 'tittle':
                    if entry.get(key) == tittle:
                        check_entry = True  
                        break
        return  check_entry

    def add_entry(self, id, tittle, body, date):
             
        entry = {
        'id': self.entries[-1]['id'] + 1,
        'tittle': tittle,
        'body': body,
        'date': date
        }
        if self.check_entry(tittle) is False:
            self.entries.append(entry)
            return "entry " + tittle + " added"
        else:
            return "A entry with the tittle'" + tittle + "' exists. Add not successful"