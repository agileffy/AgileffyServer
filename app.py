from flask import Flask, request, session, make_response
import cloudant
import hashlib

TIMEOUT=10 #fixme

app = Flask(__name__)
import os
import time
import bcrypt


@app.route('/')
def hello_world():
    return 'Hello World!'


def find_in_database(username):#fixme
    return False


def get_result_in_database(username):#fixme

    return {}


def insert_in_database(username, salt):#fixme
    pass


def update_in_database(username, md5):#fixme
    pass


def initdb():
    pass

@app.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get('db'):
        session['db']=initdb()
    if (not session.get('salt')) or request['new'] is True:
        if not find_in_database(request['username']):
            session['salt'] = os.urandom(16)
            session['username']=request['username']
            insert_in_database(session['username'], session['salt'])
            response = make_response("OK")
            response.set_cookie('salt', str(session['salt']))
            response.set_cookie('username_check', 'true')
            response.set_cookie('debug_new', 'true')
        else:
            response = make_response("Invalid Username")
            response.set_cookie('username_check', 'false')
            response.set_cookie('debug_new', 'true')
        return response
    else:
        md5 = request['md5']
        t = request['time']
        crypt = request['crypt']
        if t < time.time() - TIMEOUT:
            response = make_response("Timeout")
            response.set_cookie('time_check', 'false')
            response.set_cookie('hash_check', 'false')
            response.set_cookie('debug_new', 'false')
            return response
        if crypt != bcrypt.hashpw(md5, t):
            response = make_response("HashError")
            response.set_cookie('time_check', 'true')
            response.set_cookie('hash_check', 'false')
            response.set_cookie('debug_new', 'false')
            return response
        else:
            update_in_database(session['username'], request['md5'])
            response = make_response("OK")
            response.set_cookie('time_check', 'true')
            response.set_cookie('hash_check', 'true')
            response.set_cookie('debug_new', 'false')
            return response


@app.route('/login')
def login():
    if (not session.get('salt')) or request['new'] is True:
        if not find_in_database(request['username']):
            response = make_response("Invalid Username")
            response.set_cookie('username_check', 'false')
            response.set_cookie('debug_new', 'true')
            return response
        session['username']=request['username']
        res = get_result_in_database(session['username'])
        response = make_response("OK")
        response.set_cookie('salt', str(res['salt']))
        response.set_cookie('username_check', 'true')
        response.set_cookie('debug_new', 'true')
        session['salt'] = res['salt']
        return response
    else:
        res = get_result_in_database(session['username'])
        t = request['time']
        crypt = request['crypt']
        md5 = res['md5']
        if t < time.time() - TIMEOUT:
            response = make_response("Timeout")
            response.set_cookie('time_check', 'false')
            response.set_cookie('password_check', 'false')
            response.set_cookie('debug_new', 'false')
            return response
        if crypt != bcrypt.hashpw(md5, t):
            response = make_response("Password Wrong")
            response.set_cookie('time_check', 'true')
            response.set_cookie('password_check', 'false')
            response.set_cookie('debug_new', 'false')
            return response
        else:
            session['login'] = True
            response = make_response("Login successfully")
            response.set_cookie('time_check', 'true')
            response.set_cookie('password_check', 'true')
            response.set_cookie('debug_new', 'false')
            return response


@app.route('/create')
def init():
    # server = couchdb.Server('http://127.0.0.1:5984/')
    # db = server['agileffy-server']
    pass


if __name__ == '__main__':
    app.run(debug=True)
