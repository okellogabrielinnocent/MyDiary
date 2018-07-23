
from flask import Flask, request, jsonify
from flask import Flask
from flask import jsonify
from flask import request
from .models import Entry
import datetime

error = None
'''
Initialising a flask application
'''

app = Flask(__name__)  


'''
API end points
'''
@app.route('/api/v1/entries',methods=['GET'])
def get_entries():
    '''
    get all entries in the list
    :return: all entries
    '''
    if "application/json" not in str(request.content_type):
        return jsonify({'error': "Bad Request. JSON Request Expected"}), 400
    
    return jsonify({'entries': Entry.entries}), 200


@app.route('/api/v1/entries/<int:entryId>',methods=['GET'])
def get_entry(entryId=0):
    '''
    retrieves a single entry from the entrys database
    :param entryId:
    :return: entry
    '''
    if "application/json" not in str(request.content_type):
        return jsonify({'error': "Bad Request. JSON Request Expected"}), 400
    
    if not isinstance(entryId, int):
        return jsonify({'Server Error': 'entryId should be an integer'}), 500
    
    entry = Entry.get_entry(entryId)
    length = len(entry)
    if length == 0:
        return jsonify({'entry not found': 'Searched entry no ' + str(entryId) + " was not found"}), 404
    return jsonify({'entry': entry[0]}), 201


@app.route('/api/v1/entries/<entryId>',methods=['PUT'])
def update_entry(entryId):
    en = [ entry for entry in Entry.entries if (entry['id'] == entryId) ]
    if  not 'tittle' in request.json:
        error = 'Please wrong tittle'
        return error
    elif 'tittle' in request.json:
        en[0]['tittle'] = request.json['tittle']

    if not 'body' in request.json:
        error = 'Please wrong body'
        return error    
    elif 'body' in request.json:
        en[0]['body'] = request.json['body']

    
    if 'date' in request.json : 
        en[0]['date'] = request.json['date']
    return jsonify({'entry':en[0]}),200


@app.route('/api/v1/entries',methods=['POST'])
def create_entry():
    dat = {
    'id':request.json['id'],
    'tittle':request.json['tittle'],
    'body':request.json['body'],
    'date':request.json['date']
    }
    if  not 'tittle' and 'body' and 'id' and 'date' in request.json:
        error = 'Please enter correct details'
        return error
    elif 'tittle' and 'body' and 'id' and 'date' in request.json:
        Entry.entries.append(dat)
        return jsonify(dat),201
        