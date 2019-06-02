from flask import Flask, request, session, make_response
from cloudant import CouchDB
import hashlib
import config

app = Flask(__name__)
import os
import time
import bcrypt


@app.route('/')
def hello_world():
    return 'Hello World!'


def findInDatabase(db, username):
    result = username in db
    return result


def getResultInDatabase(db, username):
    return db[username]


def insertInDatabase(db, username, salt):
    doc = db[username]
    doc['salt'] = salt


def updateInDatabase(db, username, md5):
    doc = db[username]
    doc['md5'] = md5


def connectClient():
    client = CouchDB(config.username, config.password, url=config.url,
                     connect=True,
                     auto_renew=True)
    return client


def initDB():
    client = connectClient()

    db = client[config.database]
    return db


def createDB():
    client = connectClient()

    if not client.exists():
        print('ERROR:Can not connect client')
        return False

    db = client[config.database]

    if not db.exists():
        db = client.create_database(config.database)

    if not db.exists():
        print('ERROR:Can not create database')
        return False

    return True


@app.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get('db'):
        session['db']=initDB()
    if (not session.get('salt')) or request['new'] is True:
        if not findInDatabase(session['db'], request['username']):
            session['salt'] = os.urandom(16)
            session['username']=request['username']
            insertInDatabase(session['db'], session['username'], session['salt'])
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
        if t < time.time() - config.TIMEOUT:
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
            updateInDatabase(session['username'], request['md5'])
            response = make_response("OK")
            response.set_cookie('time_check', 'true')
            response.set_cookie('hash_check', 'true')
            response.set_cookie('debug_new', 'false')
            return response


@app.route('/login')
def login():
    if (not session.get('salt')) or request['new'] is True:
        if not findInDatabase(session['db'], session['username']):
            response = make_response("Invalid Username")
            response.set_cookie('username_check', 'false')
            response.set_cookie('debug_new', 'true')
            return response
        session['username']=request['username']
        res = getResultInDatabase(session['db'], session['username'])
        response = make_response("OK")
        response.set_cookie('salt', str(res['salt']))
        response.set_cookie('username_check', 'true')
        response.set_cookie('debug_new', 'true')
        session['salt'] = res['salt']
        return response
    else:
        res = getResultInDatabase(session['db'], session['username'])
        t = request['time']
        crypt = request['crypt']
        md5 = res['md5']
        if t < time.time() - config.TIMEOUT:
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
    if createDB():
        app.run(debug=True)
