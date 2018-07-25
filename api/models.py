import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from .database_tables import tables_list
import jwt
from flask import jsonify
import os

from datetime import datetime, timedelta

""" Variable for encoding and decoding web token """
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 9000


class Database(object):
    """

    Creates database connection and tables
    Has methods associated with database objects like
    users, entries and entry requests
    The methods are called from the views.py file

    """

    def __init__(self):
        """ Initialising a database connection """
        if os.getenv('APP_SETTINGS') == "testing":
            self.dbname = "test_db"
        else:
            self.dbname = "mydiary"

        try:
            # establishing a server connection
            self.connection = psycopg2.connect(dbname="{}".format(self.dbname),
                                               user="postgres",
                                               password="moschinogab19",
                                               host="localhost"
                                               )
            self.connection.autocommit = True

            # activate connection cursor
            self.cursor = self.connection.cursor()
        except psycopg2.Error as err:
            # bug in returning under the __init__
            print("Can not establish a database connection")

    def create_tables(self):
        """ Create database tables from the database_tables.py file """
        for data in tables_list:
            for table_name in data:
                self.cursor.execute(data[table_name])

    def should_be_unique(self,
                         username,
                         email,
                         phone_number
                         ):
        """ 
        Is a helper function that is called by other functions
        to ensure username and phone_number are unique
        """

        select_query = "SELECT username, email, phone_number FROM mydiary_users"
        self.cursor.execute(select_query)
        row = self.cursor.fetchall()
        for result in row:
            if result[0] == username:
                return jsonify({"message": "Username already taken, try another"})
            if result[1] == email:
                return jsonify({"message": "User account with that email already exists"})
            if result[2] == phone_number:
                return jsonify({"message": "User account with that phone number already exists"})

    def signup(self,
               name,
               email,
               username,
               phone_number,
               bio,
               gender,
               password
               ):

        # Check if username, email and phone_number don't exist
        if self.should_be_unique(username, email, phone_number):
            return self.should_be_unique(username, email, phone_number)

        # hash the password
        hashed_password = generate_password_hash(password, method="sha256")

        # inserting user info into the mydiary_users table
        try:
            sql = "INSERT INTO mydiary_users(name, email, username, " \
                  "phone_number, bio, gender, password) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql,
                                (name, email, username, phone_number,
                                 bio, gender, hashed_password)
                                )
        except Exception as err:
            return jsonify({"message": "Username, email or phone_number already used "})
        return jsonify({"message": "Account successfully created"})

    def sign_in(self, username, password):
        """ A sign a web token to current user if username and password match """
        try:
            # query the user table for the username and password
            select_query = "SELECT username, password, id FROM mydiary_users"
            self.cursor.execute(select_query)
            result = self.cursor.fetchall()
        except Exception as err:
            return str(err)

        # assigning a web token if info right
        for user_data in result:
            if user_data[0] == username and check_password_hash(user_data[1], password):
                payload = {
                    'id': user_data[2],
                    'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
                }
                token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
                return jsonify({"Message": token.decode('UTF-8')})

        else:
            return jsonify({"Message": "Email or password is incorrect"})

    def get_all_users(self):
        """ Returns a list of all users in the database """

        select_query = "SELECT * FROM mydiary_users"
        self.cursor.execute(select_query)
        results = self.cursor.fetchall()

        user_list = []

        for user in results:
            user_info = {}
            user_info['name'] = user[0]
            user_info['username'] = user[1]
            user_info['email'] = user[2]
            user_info['phone_number'] = user[3]
            user_info['bio'] = user[4]
            user_info['gender'] = user[5]

            user_list.append(user_info)

        return user_list

    def create_entry(self,
                    user_id,
                    tittle,
                    body,
                    creation_date,
                    update_date
                    ):
        """ Creates entry in the database
            The user_id which is a foreign key is gotten from
            the current_user instance in the token_required()
            decorator as id
        """
        try:
            sql = "INSERT INTO mydiary_entries(user_id, " \
                                             "tittle, " \
                                             "body, " \
                                             "creation_date, " \
                                             "update_date, " \
                                             "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(
                                sql,
                                (user_id, tittle, body, creation_date,
                                 update_date)
                                )
        except psycopg2.Error as err:
            return str(err)
        return "Entry created successfully"

    def get_entries(self):
        """ Returns a list of all entry offers available """

        sql = "SELECT tittle, body, creation_date, update_date, " \
              "id FROM mydiary_entries"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        entries_list = []
        for entry in result:

            entry_info = {}
            entry_info['tittle'] = entry[0]
            entry_info['body'] = entry[1]
            entry_info['creation_date'] = entry[2]
            entry_info['update_date'] = entry[3]
            entry_info['entry_id'] = entry[4]

            entries_list.append(entry_info)
        return jsonify({"Entries": entries_list})

    def entries_written(self, user_id):
        """ Returns a list of entries given by the User(user)"""
        try:
            sql = "SELECT tittle, body, creation_date, update_date, " \
                  "id FROM mydiary_entries WHERE " \
                  "user_id=%s" % user_id
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except:
            return jsonify({"Message": "Some thing went wrong"})

        entries_list = []
        for entry in result:
            entry_info = {}
            entry_info['tittle'] = entry[0]
            entry_info['body'] = entry[1]
            entry_info['creation_date'] = entry[2]
            entry_info['update_date'] = entry[3]
            entry_info['entry_id'] = entry[4]

            entries_list.append(entry_info)
        return entries_list

    def get_user_info(self, user_id):
        """ Gets the info of the user with the user_id provided"""

        sql = "SELECT username, phone_number, gender " \
              "FROM mydiary_users WHERE id=%s" % user_id

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        user = {}  # holds user information
        for user_info in result:
            user['username'] = user_info[0]
            user['gender'] = user_info[2]
            user['phone number'] = user_info[1]
        return user

    def entry_details(self, entry_id):
        """ Returns the details of a entry offer with the entry_id provided
            Also contains the user information
        """

        sql = "SELECT tittle, body, creation_date, update_date, " \
              "user_id FROM mydiary_entries WHERE id=%s" % entry_id

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if not result:
            return jsonify({"Message": "The entry offer with entry_id {} does not exist".format(entry_id)})

        entry_info = {}
        for info in result:
            # user information to be returned with entries details
            user_id = info[4]
            user_info = self.get_user_info(user_id)
            entry_info['user details'] = user_info

            entry_info['tittle'] = info[0]
            entry_info['body'] = info[1]
            entry_info['creation_date'] = info[2]
            entry_info['update_date'] = info[3]

        return jsonify({"entry details": entry_info})