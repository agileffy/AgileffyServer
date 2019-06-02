import base64
import json
import os

from flask import request, make_response

from src import app
from src.DB import DB
from src.utils import encrypt


@app.route('/api/register', methods=['POST'])
def register():
    db = DB()
    data = json.loads(request.data.decode())
    if not db.isExist(data['username']):
        username = data['username']
        salt = os.urandom(16)
        password = encrypt(data['password'], salt)
        email = data['email']
        print('DEBUG: Ready to create doc')
        if db.newDoc(dict(_id=username,
                          salt=base64.b64encode(salt).decode(),
                          password=base64.b64encode(password).decode(),
                          email=email)):
            response = make_response("OK")
            return response
            # return 'OK'
        else:
            response = make_response("An Error occured on the server")
            return response
            # return 'An Error occured on the server'
    else:
        response = make_response("Username Exists")
        return response
        # return 'Username Exists'
