from flask import Flask, request, jsonify
import jwt
from functools import wraps
from .models import Database

db_connection = Database()
""" 
Variables for encoding and decoding web token 
"""
JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'

"""
create an instance of the Database 
"""

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

            sql = "SELECT username, password, id FROM  mydiary_users WHERE id=%s" % (data['id'])
            db_connection.cursor.execute(sql)
            current_user = db_connection.cursor.fetchone()
        except Exception as ex:
            return jsonify({"Bad token message": str(ex)})

        return f(current_user, *args, **kwargs)
    return decorated