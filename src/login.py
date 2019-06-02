from src.DB import DB
from flask import request, session, make_response
from src.utils import encrypt
from src import app

@app.route('/login', methods=['GET', 'POST'])
def login():
    if not session.get('db'):
        session['db']=DB()
    db=session['db']
    res=db.findDoc(request['username'])
    if not res.exists():
        response=make_response("No such username")
        return response
    if encrypt(request['password'],res['salt'])==res['password']:
        session['login']=True
        response=make_response("OK")
        return response
    else:
        response=make_response("Password Wrong")
        return response
    