from flask import Flask, request, jsonify
from .models import Database
from .utils import token_required
import datetime
from datetime import date

app = Flask(__name__)
db_connection = Database()
today = str(date.today())



@app.route('/api/v1/auth/signup', methods=['POST'])
def create_user():
    """ Creating a user account
        calls the signup() function in models.py
    """    
    try:
        name = request.json["name"]
        email = request.json['email']
        username = request.json['username']
        phone_number = request.json['phone_number']
        bio = request.json['bio']
        gender = request.json['gender']
        password = request.json['password']

        result = db_connection.signup(name,
                                            email,
                                            username,
                                            phone_number,
                                            bio, gender,
                                            password)

        return result
    except Exception as err:
        return jsonify({"message": "The {} parameter does not exist".format(str(err))}), 400


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """ The function confirms the presence of user.
        It login the user by providing a web token
    """
    
    try:

        username = request.json['username']
        password = request.json['password']

        # sign_in now by calling the sign in message
        result = db_connection.sign_in(username, password)
        return result
    except Exception as err:
        return jsonify({"Message": "The {} parameter does not exist".format(str(err))})


@app.route('/api/v1/entries', methods=['POST'])
@token_required
def create_entry(current_user):
    try:  
        request.json['creation_date'] = today
        title = request.json['title']
        body = request.json['body']
        creation_date = request.json['creation_date']

        result = db_connection.post_entry(current_user[2],
                                                title,
                                                body,
                                                creation_date
                                                )
        return jsonify({"message": result})
    except Exception as err:
        return jsonify({"Message": "The {} parameter does not exist".format(str(err))}), 404


@app.route('/api/v1/entries', methods=['GET'])
@token_required
def available_entries(current_user):
    """ Retrieves all the available entry written """
    result = db_connection.get_entries()
    return result, 200


@app.route('/api/v1/entries/<entry_id>', methods=['GET'])
@token_required
def get_single_entry(current_user, entry_id):
    """ Retrieve a single entry by providing the entry_id """
    try:
        entry_id = int(entry_id)
        result = db_connection.entry_details(entry_id)
        return result, 200
    except:
        return jsonify({"message": "Entry id should be integer"})
    

@app.route('/api/v1/entries/<entry_id>',methods=['PUT'])
@token_required
def update_entry(current_user,entry_id):
    
    try:
        id = int(entry_id)
    except ValueError as errr:
        return jsonify(
            {"message": "Entry_id should be of type integer"}
        )
    try:
        request.json['creation_date'] = today
        title = request.json['title']
        body = request.json['body']
        creation_date = request.json['creation_date']   

        result = db_connection.update_to_entry(current_user[2], entry_id, title, body,creation_date)
        return result
    except ValueError as err:
        return jsonify({"Message": "The {} parameter does not exist".format(str(err))}), 404