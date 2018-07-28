import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from .sql import tables
import jwt
from flask import jsonify
import os

from datetime import datetime, timedelta

""" Variable for encoding and decoding web token """
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 9000


class Database(object):

    def __init__(self):
        """ Initialising a database connection """
        if os.getenv('APP_SETTINGS') == "testing":
            self.dbname = "test_db"
        else:
            self.dbname = "mydiary"

        try:
            # establish a server connection
            self.connection = psycopg2.connect(dbname="{}".format(self.dbname),
                                               user="postgres",
                                               password="moschinogab19",
                                               host="localhost"
                                               )
            self.connection.autocommit = True

            # call connection cursor
            self.cursor = self.connection.cursor()
        except psycopg2.Error as err:
            print("Can not establish a database connection")

    def create_tables(self):
        """ 
        Create database tables
        """
        for data in tables:
            for table_name in data:
                self.cursor.execute(data[table_name])

    def validate(self,
                         username,
                         email,
                         phone_number
                         ):
        
        select_query = "SELECT username, email, phone_number FROM mydiary_users"
        self.cursor.execute(select_query)
        row = self.cursor.fetchall()
        for result in row:
            if result[0] == username:
                return jsonify({"message": "Username already used, use another"})
            if result[1] == email:
                return jsonify({"message": "Email already used"})
            if result[2] == phone_number:
                return jsonify({"message": "Phone number already used"})

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
        if self.validate(username, email, phone_number):
            return self.validate(username, email, phone_number)

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
            return jsonify({"message": "username, email or phone_number already used "})
        return jsonify({"message": "Account successfully created"})

    def sign_in(self, username, password):
        
        """ 
        ceat web token in username and password is correct 
        """
        try:
            # query the user table for the username and password
            query_user = "SELECT username, password, id FROM mydiary_users"
            self.cursor.execute(query_user)
            result = self.cursor.fetchall()
        except Exception as err:
            return str(err)

        '''
        Assigning a web token if user info right to user_id =id
        '''
        for user_data in result:
            print(user_data)
            if user_data[0] == username and check_password_hash(user_data[1], password):
                payload = {
                    'id': user_data[2],
                    'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
                }
                token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
                return jsonify({"Message": token.decode('UTF-8')})

        else:
            return jsonify({"Message": "Username or password is incorrect"})
    

    def get_users(self):
        """ Returns a list of all users in the database """

        select_query = "SELECT * FROM mydiary_users"
        self.cursor.execute(select_query)
        results = self.cursor.fetchall()

        user_list = []

        for user in results:
            user_details = {}
            user_details['name'] = user[0]
            user_details['username'] = user[1]
            user_details['email'] = user[2]
            user_details['phone_number'] = user[3]
            user_details['gender'] = user[4]
            user_details['password'] = user[5]

            user_list.append(user_details)

        return user_list

    def post_entry(self,user_id,tittle,body,creation_date):
        
        try:
            sql = "INSERT INTO mydiary_entry(user_id,tittle, body, creation_date) " \
                                             "VALUES (%s, %s, %s, %s)"
            self.cursor.execute(
                                sql,
                                (user_id, tittle, body, creation_date)
                                )
        except psycopg2.Error as err:
            return str(err)
        return "Entry created successfully"

    def get_entries(self):
        """ Returns a list of all entries created """

        sql = "SELECT tittle, body, creation_date, update_date, " \
              "id FROM mydiary_entry"
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
        return jsonify({"Entries": entries_list}),200


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
        """ 
        Returns the details of a entry with user details whose id is provided
        """

        sql = "SELECT tittle, body, creation_date, update_date, " \
              "user_id FROM mydiary_entry WHERE id=%s" % entry_id

        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if not result:
            return jsonify({"Message": "The entry with entry id {} does not exist".format(entry_id)})

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