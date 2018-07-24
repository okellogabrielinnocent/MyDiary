from flask import Flask, request, jsonify
from .models import DatabaseConnection
from functools import wraps
import jwt
import datetime

app = Flask(__name__)  # Initialising a flask application

""" Variable for encoding and decoding web token """
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

"""creating an instance of the DatabaseConnections table
   used o execute run methods in the models.py
"""
database_connection = DatabaseConnection()


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

            sql = "SELECT * FROM  carpool_users WHERE id=%s" % (data['id'])
            database_connection.cursor.execute(sql)
            current_user = database_connection.cursor.fetchone()
        except Exception as ex:
            return jsonify({"message": str(ex)})

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
@token_required
def list_of_users(current_user):
    """ Get all users"""
    result = database_connection.get_all_users()
    return jsonify({"Users": result})


@app.route('/api/v1/users/entries', methods=['POST'])
@token_required
def create_entry(current_user):
    """ Creating a entry offer """

    if (not request.json or
            "body" not in request.json or
            "creation_date" not in request.json or
            "update_date" not in request.json or
            "free_spots" not in request.json or
            "contribution" not in request.json or
            'origin' not in request.json or
            'destination' not in request.json or
            "meet_point" not in request.json):

        return jsonify(
            {"message": "You have either missed out some info or used wrong keys"}
        ), 400

    origin = request.json['origin']
    destination = request.json['destination']
    meet_point = request.json['meet_point']
    contribution = request.json['contribution']
    free_spots = request.json['free_spots']
    update_date = request.json['update_date']
    creation_date = request.json['creation_date']
    body = request.json['body']

    # Checking for errors

    if not isinstance(body, str):
        return jsonify({"message": "body should be string"})

    if not isinstance(update_date, str):
        return jsonify({"message": "Start date should be string"})

    if not isinstance(creation_date, str):
        return jsonify({"message": "Finish date should be string"})

    if not isinstance(free_spots, int):
        return jsonify({"message": "Free spots should be integer"})

    if not isinstance(origin, str):
        return jsonify({"message": "Origin should be string"})

    if not isinstance(destination, str):
        return jsonify({"message": "Destination should be string"})

    if not isinstance(meet_point, str):
        return jsonify({"message": "meet_point should be string"})

    if not isinstance(contribution, (int, float, complex)):
        return jsonify({"message": "contribution should be integer"})

    result = database_connection.create_entry(current_user[0],
                                             origin, meet_point,
                                             contribution,
                                             free_spots,
                                             update_date,
                                             creation_date)
    return jsonify({"message": result})


@app.route('/api/v1/entrys', methods=['GET'])
@token_required
def available_entry(current_user):
    """ Retrieves all the available entry offers """
    result = database_connection.get_entrys()
    return result


@app.route('/api/v1/this/user/entrys', methods=['GET'])
@token_required
def driver_entrys(current_user):
    """ Retrieves all the available entry offers """
    result = database_connection.entrys_given(current_user[0])
    return jsonify({"{}'s entry offers".format(current_user[2]): result})


@app.route('/api/v1/entrys/<entry_id>', methods=['GET'])
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


@app.route('/api/v1/entrys/<entry_id>/requests', methods=['POST'])
@token_required
def request_for_entry(current_user, entry_id):
    """ Passenger can request for a entry by providing the entry_id"""
    try:
        entry_id = int(entry_id)
    except ValueError as exc:
        return jsonify(
            {"message": "entry_id should be of type integer"}
        )
    result = database_connection.request_entry(current_user[0], entry_id)
    return result


@app.route('/api/v1/users/entrys/<entry_id>/requests', methods=['GET'])
@token_required
def requests_to_this_entry(current_user, entry_id):
    """ Retrieves all entry requests for that entry offer with id passed in """
    try:
        entry_id = int(entry_id)
    except ValueError as exc:
        return jsonify(
            {"message": "entry_id should be of type integer"}
        )
    if not isinstance(entry_id, int):
        return jsonify({"message": "entry_id should be of type integer"})

    result = database_connection.requests_to_this_entry(current_user[0], entry_id)
    return result


@app.route('/api/v1/users/entrys/<request_id>/reaction', methods=['PUT'])
@token_required
def reaction_to_entry_request(current_user, request_id):
    """ Driver accepts or rejects a entry request """
    try:
        request_id = int(request_id)
    except ValueError as exc:
        return jsonify(
            {"message": "request_id should be of type integer"}
        )
    if not isinstance(request_id, int):
        return jsonify({"message": "request_id should be of type integer"})

    if not request.json or 'reaction' not in request.json:
        return jsonify(
            {
                "message":
                "Input should be of type dictionary where key is 'reaction' and"
                " value 'reject' or 'accept' or 'pending' set back to default"
            }
        ), 400

    status = request.json['reaction']
    # changing the status of a request
    if status == 'reject':
        status = 'rejected'
    if status == 'accept':
        status = 'accepted'
    if status == 'pending':
        status = 'pending'

    result = database_connection.respond_to_request(current_user[0], request_id, status)
    return result






