import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from .sql import tables
import jwt
from flask import jsonify
import os
import datetime
from datetime import date

from datetime import datetime, timedelta

""" Variable for encoding and decoding web token """
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 9000
DB_PASS = os.environ.get('DB_PASS')
today = str(date.today())



class Database(object):

    def __init__(self):
        """ Initialising a database connection """
        if not os.getenv('APP_SETTINGS') == "TESTING":
            self.dbname = "test_db"
        else:
            self.dbname = "mydiary"

        try:
            """establish a server connection"""
            
            self.connection = psycopg2.connect(dbname="{}".format(self.dbname),
                                               user= "postgres",
                                               password= DB_PASS,
                                               host="localhost"
                                               )
            self.connection.autocommit = True


            """establish a server connection on heroku"""

            """DATABASE_URL = os.environ["DATABASE_URL"]
            self.connection = psycopg2.connect(DATABASE_URL, sslmode='require')"""

            # call connection cursor
            self.cursor = self.connection.cursor()
        except psycopg2.Error as err:
            print("Can not establish a database connection")

    def create_tables(self):
        """ 
        Create database tables
        """
        for data in tables:
            self.cursor.execute(data)

    def validate_user(self,
                         username,
                         email
                         ):
        
        select_query = "SELECT username, email FROM mydiary_users"
        self.cursor.execute(select_query)
        row = self.cursor.fetchall()
        msg =""
        for result in row:
            if result[0] == username:
                msg = "Username already taken, try another"
                return msg
                
            if result[1] == email:
                msg = "Email already used"
                return msg
        return msg

                    
    def signup(self,
               name,
               email,
               username,
               phone_number,
               bio,
               gender,
               password
               ):

        """Check if username and email  don't exist"""
        if self.validate_user(username, email):
            return self.validate_user(username, email)

        """Hash the password"""
        hashed_password = generate_password_hash(password, method="sha256")

        """inserting user info into the mydiary_users table"""
        
        try:
            sql = "INSERT INTO mydiary_users(name, email, username, " \
                  "phone_number, bio, gender, password) " \
                  "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(sql,
                                (name, email, username, phone_number,
                                 bio, gender, hashed_password)
                                )
        except Exception as err:
            return jsonify({"message": "Phone_number already used "}), 400
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
            if user_data[0] == username and check_password_hash(user_data[1], password):
                payload = {
                    'id': user_data[2],
                    'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
                }
                token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
                return jsonify({"Message": token.decode('UTF-8')})

        else:
            
            return jsonify({"Message": "Username or password is incorrect"}),400
    

    
    def post_entry(self,user_id,title,body,creation_date):
        """method to create an entry"""

        try:            
            sql_query ="""SELECT * FROM mydiary_entry WHERE user_id = %s AND title = %s AND
                            body = %s"""
            self.cursor.execute(sql_query, (user_id, title, body))
            result = self.cursor.rowcount
            print(result)
            
            if result > 0:                
                response = "Entry already exists"
                return response

        
            else:
                sql = "INSERT INTO mydiary_entry(user_id,title, body, creation_date) " \
                                             "VALUES (%s, %s, %s, %s)"
                self.cursor.execute(
                                    sql,
                                    (user_id, title, body, creation_date)
                                    )
        except psycopg2.Error as err:
            return str(err)
        return "Entry created successfully"

    
    def get_entries(self):
        """ Returns a list of all entries created """

        sql = "SELECT title, body, creation_date, update_date, " \
              "id FROM mydiary_entry"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        entries_list = []
        for entry in result:

            entry_info = {}
            entry_info['title'] = entry[0]
            entry_info['body'] = entry[1]
            entry_info['creation_date'] = entry[2]
            entry_info['entry_id'] = entry[4]

            entries_list.append(entry_info)
        return jsonify({"Entries": entries_list})


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

        sql = "SELECT title, body, creation_date, update_date, " \
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
            entry_info['title'] = info[0]
            entry_info['body'] = info[1]
            entry_info['creation_date'] = info[2]
        
        return jsonify(entry_info)

        """return jsonify({"entry details": entry_info})"""

    def update_to_entry(self,
                           current_user,
                           entry_id,
                           title,
                           body,
                           creation_date
                           ):
        # check for the presence of that entry id
        sql = "SELECT title,body,creation_date, user_id FROM mydiary_entry WHERE id={}"\
              .format(entry_id)
        self.cursor.execute(sql)

        result = self.cursor.fetchall()
        if not result:
            return jsonify(
                {
                    "message": "No entry with id {}".format(entry_id)
                }
            )

        # getting the entry_id to the entry where the entry was made
        # result is of length one
        entry_id = result[0][-1]

        # ensure that the current user actually created that entry
        sql = "SELECT * FROM mydiary_entry WHERE id={} AND user_id={}"\
              .format(entry_id, current_user)

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        if not result:
            return jsonify({"message":"Sorry, you are only allowed update entry you created"})

        sql = "UPDATE mydiary_entry SET title='{}',body='{}', creation_date='{}' WHERE id={}"\
              .format(title, body, creation_date, entry_id)

        self.cursor.execute(sql)

        return jsonify({"message": "Entry with id {} updated successfully".format(entry_id)}),200