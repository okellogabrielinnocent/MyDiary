from flask import Flask, request, jsonify
from .models import Database
from functools import wraps
import jwt
import datetime
from datetime import date

app = Flask(__name__)

""" 
Variables for encoding and decoding web token 
"""
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

"""
create an instance of the Database 
"""
database_connection = Database()


def token_required(f):
    """ Restricts access to only logged in i.e users with the right token """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            '''token = request.headers['Authorization']
            Pass token to the header
            '''
            token = request.headers.get('Authorization')

        if not token:
            return jsonify({"message": "Token missing"})


        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

            sql = "SELECT username, password FROM  mydiary_users WHERE id=%s" % (data['id'])
            database_connection.cursor.execute(sql)
            current_user = database_connection.cursor.fetchone()
        except Exception as ex:
            return jsonify({"Bad token message": str(ex)})

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
            {"message": "Please add all infromation"}
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
            {"message": "Please Fill in all the correct information"}
        ), 400

    username = request.json['username']
    password = request.json['password']

    # sign_in now by calling the sign in message
    result = database_connection.sign_in(username, password)
    return result



@app.route('/api/v1/users', methods=['GET'])
@token_required
def list_of_users(current_user):
    """ Get all users from databse"""
    result = database_connection.get_all_users()
    return jsonify({"Avilable users": result})

@app.route('/api/v1/entries', methods=['POST'])
@token_required
def create_entry(current_user):
    
    
    if (not request.json or
            "body" not in request.json or
            "tittle" not in request.json):

        return jsonify(
            {"message": "Please use correct information"}
        ), 400
    """
    Creating a entry with auto date 
    """
    
    today = str(date.today())
    request.json['creation_date'] = today

    tittle = request.json['tittle']
    body = request.json['body']
    creation_date = request.json['creation_date']

    # validations

    if not isinstance(body, str):
        return jsonify({"message": "Body should be string"})

    '''if not isinstance(update_date, str):
        return jsonify({"message": "Creation date should be string"})'''

    if not isinstance(creation_date, str):
        return jsonify({"message": "Update  should be string and of same day as create date"})

    result = database_connection.post_entry(current_user,
                                            tittle,
                                            body,
                                            creation_date
                                            )
    return jsonify({"message": result})


@app.route('/api/v1/entries', methods=['GET'])
def available_entries():
    """ Retrieves all the available entry written """
    result = database_connection.get_entries()
    return result


@app.route('/api/v1/entries', methods=['GET'])
@token_required
def user_entries(current_user):
    """ Retrieves all the available entry written """
    result = database_connection.entries_written(current_user)
    return jsonify({"{}'s entry written".format(current_user[""]): result})


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