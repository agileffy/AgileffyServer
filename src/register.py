from src.DB import DB
import os
from flask import request, session, make_response
from src.utils import encrypt
from src import app
import base64
import json


@app.route('/api/register', methods=['POST'])
def register():
    db = DB()
    print(request.data)
    print(request.data.decode())
    data = json.loads(request.data.decode())
    print(data)
    if not db.isExist(data['username']):
        username=data['username']
        salt=os.urandom(16)
        password=encrypt(data['password'],salt)
        email=data['email']
        print('DEBUG: Ready to create doc')
        if db.newDoc(dict(_id=username,
                          salt=base64.b64encode(salt).decode(),
                          password=base64.b64encode(password).decode(),
                          email=email)):
            response=make_response("OK")
            return response
            # return 'OK'
        else:
            response=make_response("An Error occured on the server")
            return response
            # return 'An Error occured on the server'
    else:
        response=make_response("Username Exists")
        return response
        # return 'Username Exists'