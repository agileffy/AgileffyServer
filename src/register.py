from src.DB import DB
import os
from flask import request, session, make_response
from src.utils import encrypt
from src import app


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get('db'):
        session['db']=DB()
    db=session['db']
    if not db.isExist(request['username']):
        username=request['username']
        salt=os.urandom(16)
        password=encrypt(request['password'],salt)
        email=request['email']
        if db.newDoc(dict(username=username,salt=salt,password=password,email=email)):
            response=make_response("OK")
            return response
        else:
            response=make_response("An Error occured on the server")
            return response
    else:
        response=make_response("Username Exists")
        return response