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

    if  "name" not in request.json:
        error = 'Please define name and it should be string'
        return jsonify({"message": error}), 400
    
    if "email" not in request.json:
        error = 'Email is not defined'
        return jsonify({"message": error}), 400

    if  "username" not in request.json:
        error = 'Username not defined'
        return jsonify({"message": error}), 400

    if  "phone_number" not in request.json:
        error = 'Phone_number not defined'
        return jsonify({"message": error}), 400

    if  "bio" not in request.json:
        error = 'Please bio is not defined'
        return jsonify({"message": error}), 400
    
    if "password" not in request.json:
        error = 'Password not defined'
        return jsonify({"message": error}), 400
    

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


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """ The function confirms the presence of user.
        It login the user by providing a web token
    """
        
    if  "username" not in request.json:
        error = 'Username not defined'
        return jsonify({"message": error}), 400
    
    if "password" not in request.json:
        error = 'Password not defined'
        return jsonify({"message": error}), 400
    

    username = request.json['username']
    password = request.json['password']

    # sign_in now by calling the sign in message
    result = db_connection.sign_in(username, password)
    return result


@app.route('/api/v1/entries', methods=['POST'])
@token_required
def create_entry(current_user):
    
    '''if  "body" not in request.json:
        error = 'body is not defined'
        return jsonify({"message": error}), 400
    
    if "title" not in request.json:
        error = 'title not defined'
    '''
    """
    Creating a entry with auto date 
    """
        
    request.json['creation_date'] = today

    title = request.json['title']
    body = request.json['body']
    creation_date = request.json['creation_date']

    """validations"""

    if not isinstance(body, str):
        return jsonify({"message": "Body should be string"})


    if not isinstance(creation_date, str):
        return jsonify({"message": "Update  should be string and of same day as create date"})

    result = db_connection.post_entry(current_user[2],
                                            title,
                                            body,
                                            creation_date
                                            )
    return jsonify({"message": result}),201


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
    except:
        return jsonify({"message": "Entry id should be integer"})

    if not isinstance(entry_id, int):
        return jsonify({"message": "Entry id should integer"})
    else:
        result = db_connection.entry_details(entry_id)
        return result, 200

@app.route('/api/v1/entries/<entry_id>',methods=['PUT'])
@token_required
def update_entry(current_user,entry_id):
    
    try:
        id = int(entry_id)
    except ValueError as errr:
        return jsonify(
            {"message": "Entry_id should be of type integer"}
        )

    if not request.json or 'title' not in request.json:
        return jsonify({"message":"You can only edit title"}), 400
    
    if not request.json or 'body' not in request.json:
        return jsonify({"message":"You can only edit body"}), 400

    request.json['creation_date'] = today
    title = request.json['title']
    body = request.json['body']
    creation_date = request.json['creation_date']   

    result = db_connection.update_to_entry(current_user[2], entry_id, title, body,creation_date)
    return result