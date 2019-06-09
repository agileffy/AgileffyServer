from src.DB import DB
from flask import request, session, make_response
from src.utils import encrypt
from src import app
import base64
import json


@app.route('/api/login', methods=['POST'])
def login():
    print(request.data)
    print(request.data.decode())
    data = json.loads(request.data.decode())
    db = DB()
    if not db.isExist(data['username']):
        response=make_response("No such username")
        return response
    res=db.findDoc(data['username'])
    print(base64.b64decode(res['salt'].encode()))
    print(base64.b64decode(res['password'].encode()))
    tmp = encrypt(data['password'],
                  base64.b64decode(res['salt'].encode()))
    if base64.b64encode(tmp).decode() == res['password']:
        session['login']=True
        response=make_response("OK")
        return response
    else:
        response=make_response("Password Wrong")
        return response
