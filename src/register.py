from src.DB import DB
import os
from flask import request, session, make_response
from src.utils import encrypt
from src import app
import base64


@app.route('/register', methods=['POST'])
def register():
    # if not session.get('db'):
    #     session['db']=DB()
    # db=session['db']
    db = DB()
    print('DEBUG:' + request.form['username'])
    print('DEBUG:' + request.form['password'])
    if not db.isExist(request.form['username']):
        username=request.form['username']
        salt=os.urandom(16)
        password=encrypt(request.form['password'],salt)
        email=request.form['email']
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