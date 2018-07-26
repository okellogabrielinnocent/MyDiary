from api import views
import unittest
import json
import jwt

""" Variable for encoding and decoding web token """
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

BASE_URL = '/api/v1/'
content_type = 'application/json'


class Diary(unittest.TestCase):
    
    def setUp(self):
        # views.app.config['TESTING'] = True
        self.app = views.app.test_client()
        self.cur = views.database_connection
        views.database_connection.create_tables()

        # --------***** Creating users ********------------------

        # second user instance
        self.user_1 = {
            "name": "gabriel",
            "email": "okellogabrielinnocent.com",
            "username": "gabriel",
            "phone_number": "o756514003",
            "bio": "This is gabriel, software engineer",
            "gender": "Male",
            "password": "innocorp"
        }

        # second user instance
        self.user_2 = {
            "name": "gabriel",
            "email": "okellogabrielinnocent@gmail.com",
            "username": "gabriel_2",
            "phone_number": "o756514003",
            "bio": "This is gabriel, software engineer",
            "gender": "Male",
            "password": "innocorp"
        }

        # wrong and missing parameters
        self.user_3 = {
            "name_3": "gabriel",
            "email": "okellogabrielinnocent.com",
            "username_3": "gabriel_3",
            "bio": "This is gabriel, software engineer",
            "gender_3": "Male",
            "password": "innocorp"
        }

        # ---------------- Testing the user login --------------------

        # This user exists
        self.login_user_1 = {
            "username": "gabriel",
            "password": "innocorp"
        }
        # This user does not exist
        self.login_user_2 = {
            "username": "gabriel_2",
            "password": "innocorp"
        }

        # This user does not exist
        self.login_user_404 = {
            "username": "gabriel_404",
            "password": "innocorp"
        }

        # Bad request 400 | wrong inputs (keys)
        self.login_user_400 = {
            "username_400": "gabriel_400",
            "password": "innocorp"
        }

        # ----------------- Create entry  ---------------------

        self.entry_1 = {"tittle": "Andela",
                       "body": "It's time to join the Andela community",
                       "creation_date": "21st/06/2018",
                       "update_date": "1st/06/2018"
                       }

        self.entry_2 = {"tittle": "Growth Mindset",
                       "body": "Andela",
                       "creation_date": "21st/06/2018",
                       "update_date": "1st/06/2018"
                       }
        

        self.entry_400 = {"tittle_400": "Growth Mindset",
                         "body_400": "Andela",
                         "creation_date": "21st/06/2018",
                         "update_date": "1st/06/2018",
                         }

        

    # ********** Test whether the endpoints are protected ****************


    def test_create_entry_protected(self):
        """ Confirm list_of_users endpoint is protected
            It lists all users in the application
        """
        response = self.app.post('{}users/entries'.format(BASE_URL),
                                 content_type=content_type)
        self.assertEqual(response.json, {"Message": "Token missing"})

    

    '''"""def test_user_entries_protected(self):
        """ Confirm user_entry endpoint is protected
            It lists all entry given by the current user
        """
        response = self.app.get('{}this/user/entries'.format(BASE_URL),
                                content_type=content_type)
        self.assertEqual(response.json, {"Message": "Token missing"})"""
'''
    
    
        

    # ************** Test Signup **************************************************

    def test_create_user_1(self):
            """ Creating a user | supply right data
                expect a success
            """
            response = self.app.post("{}auth/signup".format(BASE_URL),
                                     data=json.dumps(self.user_1),
                                     content_type=content_type)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json,
                             {"message": "Account successfully created"})

    def test_create_user_same_username(self):
        """ Creating another user with the same username """
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # Creating another user with the same username, email and password
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)
        self.assertEqual(response.json,
                         {'message': 'Username already taken, try another'})

    def test_create_user_3(self):
        """ Second user instance | all expected to work fine """
        response_2 = self.app.post("{}auth/signup".format(BASE_URL),
                                   data=json.dumps(self.user_2),
                                   content_type=content_type)
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(response_2.json,
                         {"message": "Account successfully created"})  # length=2

    def test_create_user_4(self):
        """ Wrong and missing user fields | Should raise and error Message """
        response_3 = self.app.post("{}auth/signup".format(BASE_URL),
                                   data=json.dumps(self.user_3),
                                   content_type=content_type)

        self.assertEqual(response_3.status_code, 400)
        self.assertEqual(response_3.json,
                         {"message": "You have either missed out some info or used wrong keys"})

    # ************************* Test Login **********************************

    def test_login_1(self):
        # ---- for bad request ---------------------------
        """ Supply wrong data e.g missing fields"""
        response_400 = self.app.post("{}auth/login".format(BASE_URL),
                                     data=json.dumps(self.login_user_400),
                                     content_type=content_type)
        self.assertEqual(response_400.status_code, 400)

    def test_login_account(self):
        """ Right data but account does not exist """
        response_1 = self.app.post("{}auth/login".format(BASE_URL),
                                   data=json.dumps(self.login_user_1),
                                   content_type=content_type)

        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_1.json, {'Message': 'Email or password is incorrect'})

    def test_login_2(self):
        """ create a user and login with with username which
            does not exist
         """

        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_2),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'Message': 'Email or password is incorrect'})

    def test_login_3(self):
        """ Lets creates a user and then login expect a success """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

    # ****************** Test create entry ********************************

    def test_create_entry_1(self):
        """ Lets create a entry offer here, first create account login and create entry
            Supply right entry data expect a success Message
        """

        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Message']

        # supply right information
        response = self.app.post('{}users/entries'.format(BASE_URL),
                                 data=json.dumps(self.entry_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"Message": "entry create successfully"})

    # Lets try creating a entry but supply wrong data
    def test_create_entry_2(self):
        """ Supply wrong data when creating a entry by the logged in user"""
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Message']

        # supply information with wrong keys and missing parameters
        response = self.app.post('{}users/entries'.format(BASE_URL),
                                 data=json.dumps(self.entry_400),
                                 headers={'Authorization': self.token}, content_type=content_type)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'Message': 'You have either missed out some info or used wrong keys'})

    # Lets try creating a entry but supply wrong data
    def test_create_entry_wrong(self):
        """ Supply wrong data when creating a entry by the logged in user
            with contribution as a string
        """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Message']

        

    # ************ Test available entries **********************************

    def test_available_entry(self):
        """ Create a user , login and then create a entry """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Message']

        # supply right information
        response = self.app.post('{}users/entries'.format(BASE_URL),
                                 data=json.dumps(self.entry_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"Message": "entry create successfully"})

        # supply right information
        response = self.app.post('{}users/entries'.format(BASE_URL),
                                 data=json.dumps(self.entry_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"Message": "entry create successfully"})

        # check for the number of entries present
        response = self.app.get('{}entries'.format(BASE_URL), headers={'Authorization': self.token}, content_type=content_type)

        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(len(response.json['entries']), 2)

    # ************* Test user entries *******************************

    def test_user_entries(self):
        """ Create a user , login and then create a entry """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Message']
        data = jwt.decode(self.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        sql = "SELECT * FROM  mydiary_users WHERE id=%s" % (data['id'])
        self.cur.cursor.execute(sql)
        self.current_user = self.cur.cursor.fetchone()

        # supply right information
        response = self.app.post('{}users/entries'.format(BASE_URL),
                                 data=json.dumps(self.entry_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"message": "entry create successfully"})

        # supply right information
        response = self.app.post('{}users/entries'.format(BASE_URL),
                                 data=json.dumps(self.entry_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"Message": "entry create successfully"})

        # check for the number of entries present
        response = self.app.get('{}this/user/entries'.format(BASE_URL), headers={'Authorization': self.token}, content_type=content_type)

        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(len(response.json["{}'s entry offers".format(self.current_user[2])]), 2)

    # *********** Test get single entry by id ***************************

    def test_get_single_entry_1(self):
        """ Create a user , login and then create a entry
            Supply wrong url input
         """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Message']
        data = jwt.decode(self.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        sql = "SELECT * FROM  mydiary_users WHERE id=%s" % (data['id'])
        self.cur.cursor.execute(sql)
        self.current_user = self.cur.cursor.fetchone()

        # supply right information
        response = self.app.post('{}users/entries'.format(BASE_URL),
                                 data=json.dumps(self.entry_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"Message": "entry create successfully"})

        # supply right information
        response = self.app.post('{}users/entries'.format(BASE_URL),
                                 data=json.dumps(self.entry_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"Message": "entry create successfully"})

        # check for the number of entries present
        response = self.app.get('{}entries/<entry_id>'.format(BASE_URL), headers={'Authorization': self.token}, content_type=content_type)

        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {'Message': 'Input should be integer'})

    def test_get_single_entry_2(self):
        """ Create a user , login and then create a entry
            Supply wrong url input
         """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Message']
        data = jwt.decode(self.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        sql = "SELECT * FROM  mydiary_users WHERE id=%s" % (data['id'])
        self.cur.cursor.execute(sql)
        self.current_user = self.cur.cursor.fetchone()

        # supply right information
        response = self.app.post('{}users/entries'.format(BASE_URL),
                                 data=json.dumps(self.entry_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"Message": "entry create successfully"})

        # supply right information
        response = self.app.post('{}users/entries'.format(BASE_URL),
                                 data=json.dumps(self.entry_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"Message": "entry create successfully"})

        # check for the number of entries present
        response = self.app.get('{}entries/<entry_id>'.format(BASE_URL), headers={'Authorization': self.token}, content_type=content_type)

        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(len(response.json), 1)

    def test_get_single_entry_3(self):
        """ Create a user , login and then create a entry
            entry id which does not exist
         """
        # Creating a user instance, length is one
        response = self.app.post("{}auth/signup".format(BASE_URL),
                                 data=json.dumps(self.user_1),
                                 content_type=content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,
                         {"message": "Account successfully created"})

        # logging the user in
        response = self.app.post("{}auth/login".format(BASE_URL),
                                 data=json.dumps(self.login_user_1),
                                 content_type=content_type)
        self.assertEqual(response.status_code, 200)

        # capturing the token
        self.token = response.json['Message']
        data = jwt.decode(self.token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        sql = "SELECT * FROM  mydiary_users WHERE id=%s" % (data['id'])
        self.cur.cursor.execute(sql)
        self.current_user = self.cur.cursor.fetchone()

        # supply right information
        response = self.app.post('{}users/entries'.format(BASE_URL),
                                 data=json.dumps(self.entry_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"Message": "entry create successfully"})

        # supply right information
        response = self.app.post('{}users/entries'.format(BASE_URL),
                                 data=json.dumps(self.entry_1),
                                 headers={'Authorization': self.token}, content_type=content_type)
        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"Message": "entry create successfully"})

        # check for the number of entries present
        response = self.app.get('{}entries/4'.format(BASE_URL), headers={'Authorization': self.token}, content_type=content_type)

        # self.assertEqual(response_400.status_code, 400)
        self.assertEqual(response.json, {"Message": "The entry offer with entry_id {} does not exist".format(4)})

           
    def tearDown(self):
        sql_entry = "DROP TABLE IF EXISTS mydiary_entry"
        sql = "DROP TABLE IF EXISTS mydiary_users"

        sql_list = [sql_entry, sql]
        for sql in sql_list:
            self.cur.cursor.execute(sql)