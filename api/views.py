from flask import Flask, request, jsonify
from flask import Flask
from flask import jsonify
from flask import request
from .models import Entry
import datetime
'''
Initialising a flask application
'''

app = Flask(__name__)  

'''
API end points
'''
@app.route('/api/v1/entries',methods=['GET'])
def get_all_entries():
    return jsonify({'Entries':Entry.entries}),200


@app.route('/api/v1/entries/<entryId>',methods=['GET'])
def get_entry(entryId):
    entryy = [ entry for entry in Entry.entries if (entry['id'] == entryId) ] 
    return jsonify({'entry':entryy}),200


@app.route('/api/v1/entries/<entryId>',methods=['PUT'])
def update_entry(entryId):
    data = request.get_json()
    en = [ entry for entry in Entry.entries if (entry['id'] == entryId) ]
    if  not 'tittle' in data:
        error = 'Please wrong tittle'
        return error
    elif 'tittle' in data:
        en[0]['tittle'] = data['tittle']

    if not 'body' in data:
        error = 'Please wrong body'
        return error    
    elif 'body' in data:
        en[0]['body'] = data['body']

    
    if 'date' in data : 
        en[0]['date'] = data['date']
    return jsonify({'entry':en[0]}),201


@app.route('/api/v1/entries',methods=['POST'])
def create_entry():
    data = request.get_json()
    dat = {
    'id':data['id'],
    'tittle':data['tittle'],
    'body':data['body'],
    'date':data['date']
    }
    if  not 'tittle' and 'body' and 'id' and 'date' in data:
        error = 'Please enter correct details'
        return error
    elif 'tittle' and 'body' and 'id' and 'date' in data:
        Entry.entries.append(dat)
        return jsonify(dat),201
