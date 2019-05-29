from server import server
from cloudant.client import CouchDB


@server.route('/')
@server.route('/index')
def index():
    return 'Hello World!'


@server.route('/init')
def init():
    client = CouchDB('admin', '123456', url='http://127.0.0.1:5984',
                     connect=True,
                     auto_renew=True)

    db = client['agileffy_users']

    if not db.exists():
        db = client.create_database('agileffy_users')

    if db.exists():
        return 'SUCCESS!!'
    else:
        return 'ERROR:Can not create database!'
