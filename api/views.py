
from flask import Flask, request, jsonify
from flask import Flask
from flask import jsonify
from flask import request
from .models import entries
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
def get_all_entries():
    return jsonify({'Entries':entries}),200


@app.route('/api/v1/entries/<entryId>',methods=['GET'])
def get_entry(entryId):
    entryy = [ entry for entry in entries if (entry['id'] == entryId) ] 
    return jsonify({'entry':entryy}),200


@app.route('/api/v1/entries/<entryId>',methods=['PUT'])
def update_entry(entryId):
    en = [ entry for entry in entries if (entry['id'] == entryId) ]
    if  not 'title' in request.json:
        error = 'Please wrong tittle'
        return error
    elif 'title' in request.json:
        en[0]['title'] = request.json['title']

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
    'title':request.json['title'],
    'body':request.json['body'],
    'date':request.json['date']
    }
    if  not 'title' and 'body' and 'id' and 'date' in request.json:
        error = 'Please enter correct details'
        return error
    elif 'title' and 'body' and 'id' and 'date' in request.json:
        entries.append(dat)
        return jsonify(dat),201
        