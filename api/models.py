from flask import jsonify
import os
import re
from flask import Flask, jsonify, request
from utilities.validations import ValidateInputs

class Entry:
    '''
    lets have lists of entries 
    '''
    entries=[ ]


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

    def update_entry(self, entryId=None, tittle=None,
                    body=None, date=None):
        '''
        updates the entry on index id
        :param entryId:
        :param tittle:
        :param body:
        :param date:
        :return:
        '''
        if entryId is None or entryId == "":
            return "entry id must be specified"
        if not isinstance(id, int):
            return "entry Id must be an Integer"
        if tittle is None and date is None and body is None:
            return "Either or all of entry tittle, body, date or quantity must be provided"
        entry = [entry for entry in self.entries if entry['id'] == entryId]
        if ValidateInputs.is_valid_entry_date(date)[0] == True:
            entry[0]['date'] = date
        if ValidateInputs.is_valid_entry_tittle(tittle)[0] == True:
            entry[0]['tittle'] = tittle
        if ValidateInputs.is_valid_body_tittle(body)[0] == True:
            entry[0]['body'] = body
        return "entry updated"

    def get_entry(self, entryid=None):
        '''
        searches all entries and retrieves a entry whose index is entryid
        :param entryid:
        :return:
        '''
        if entryid is None or entryid == "":
            return "entry id must be specified"
        if not isinstance(entryid, int):
            return "entry Id must be an Integer"
        entry = [entry for entry in self.entries if entry['id'] == entryid]
        if entry is not None and entry is not []:
            return entry
        return "Entry not found"
