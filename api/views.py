from flask import Flask, request, jsonify
from .models import Database
from functools import wraps
import jwt
import datetime
from datetime import date

app = Flask(__name__)

""" Variable for encoding and decoding web token """
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

"""creating an instance of the Database table
   used o execute run methods in the models.py
"""
database_connection = Database()


def token_required(f):
    """ Restricts access to only logged in i.e users with the right token """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({"message": "Token missing"})


        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

            sql = "SELECT username, password FROM  mydairy_users WHERE id=%s" % (data['id'])
            database_connection.cursor.execute(sql)
            current_user = database_connection.cursor.fetchone()
        except Exception as ex:
            return jsonify({"Message Token": str(ex)})

        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/api/v1/auth/signup', methods=['POST'])
def create_user():
    """ Creating a user account
        calls the signup() func in models.py
    """

    if (not request.json or
            "name" not in request.json or
            "email" not in request.json or
            "username" not in request.json or
            "phone_number" not in request.json or
            "bio" not in request.json or
            "gender" not in request.json or
            "password" not in request.json):

        return jsonify(
            {"message": "You have either missed out some info or used wrong keys"}
        ), 400

    name = request.json["name"]
    email = request.json['email']
    username = request.json['username']
    phone_number = request.json['phone_number']
    bio = request.json['bio']
    gender = request.json['gender']
    password = request.json['password']

    result = database_connection.signup(name,
                                        email,
                                        username,
                                        phone_number,
                                        bio, gender,
                                        password)

    return result


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    """ The function confirms the presence of user.
        It login s in the user by providing a web token
    """

    if (not request.json or
            "username" not in request.json or
            "password" not in request.json):
        return jsonify(
            {"message": "You have either missed out some info or used wrong keys"}
        ), 400

    username = request.json['username']
    password = request.json['password']

    # sign_in now
    result = database_connection.sign_in(username, password)
    return result



@app.route('/api/v1/users', methods=['GET'])
def list_of_users():
    """ Get all users"""
    result = database_connection.get_all_users()
    return jsonify({"Users": result})

@app.route('/api/v1/users/entries', methods=['POST'])
@token_required
def create_entry(current_user):
    
    
    if (not request.json or
            "body" not in request.json or
            "creation_date" not in request.json or
            "update_date" not in request.json or
            "tittle" not in request.json):

        return jsonify(
            {"message": "You have either missed out some info or used wrong keys"}
        ), 400
        """ Creating a entry offer """
        
        today = str(date.today())
        request.json['creation_date'] = today

        tittle = request.json['tittle']
        update_date = request.json['update_date']
        creation_date = request.json['creation_date']
        body = request.json['body']

    # validations

    if not isinstance(body, str):
        return jsonify({"message": "body should be string"})

    if not isinstance(update_date, str):
        return jsonify({"message": "Start date should be string"})

    if not isinstance(creation_date, str):
        return jsonify({"message": "Finish date should be string"})

    result = database_connection.create_entry(current_user[0],
                                            tittle,
                                            body,
                                            update_date,
                                            creation_date)
    return jsonify({"message": result})


@app.route('/api/v1/entries', methods=['GET'])
@token_required
def available_entries(current_user):
    """ Retrieves all the available entry offers """
    result = database_connection.get_entries()
    return result


@app.route('/api/v1/this/user/entries', methods=['GET'])
@token_required
def user_entries(current_user):
    """ Retrieves all the available entry offers """
    result = database_connection.entries_written(current_user[0])
    return jsonify({"{}'s entry offers".format(current_user[2]): result})


@app.route('/api/v1/entries/<entry_id>', methods=['GET'])
@token_required
def get_single_entry(current_user, entry_id):
    """ Retrieve a single entry by providing the entry_id """
    try:
        entry_id = int(entry_id)
    except:
        return jsonify({"message": "Input should be integer"})

    if not isinstance(entry_id, int):
        return jsonify({"message": "Input should integer"})
    else:
        result = database_connection.entry_details(entry_id)
        return result