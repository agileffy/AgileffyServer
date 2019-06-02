from src.DB import DB
from flask import request, session, make_response
from src.utils import encrypt
from src import app
import base64

@app.route('/login', methods=['POST'])
def login():
    # if not session.get('db'):
    #     session['db']=DB()
    # db=session['db']
    db = DB()
    if not db.isExist(request.form['username']):
        response=make_response("No such username")
        return response
    res=db.findDoc(request.form['username'])
    print(base64.b64decode(res['salt'].encode()))
    print(base64.b64decode(res['password'].encode()))
    tmp = encrypt(request.form['password'],
                  base64.b64decode(res['salt'].encode()))
    if base64.b64encode(tmp).decode() == res['password']:
        session['login']=True
        response=make_response("OK")
        return response
    else:
        response=make_response("Password Wrong")
        return response
    