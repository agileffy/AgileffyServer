from server import server
from cloudant.client import CouchDB


@server.route('/')
@server.route('/index')
def index():
    return 'Hello World!'


@server.route('/register', methods=['POST'])
def register():
    client = CouchDB('admin', '123456', url='http://127.0.0.1:5984',
                     connect=True,
                     auto_renew=True)

    db = client['agileffy_users']

    if not db.exists():
        return 'ERROR:No init! Please /init first!'

    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    user_exists = username in db

    if user_exists:
        return 'ERROR:Username exists!'

    data = {
        '_id': username,
        'password': password,
        'email': email
    }

    user = db.create_document(data)

    if user.exists():
        return 'SUCCESS!!'
    else:
        return 'ERROR:Database error'


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
