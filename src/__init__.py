from flask import Flask
import os
from datetime import timedelta


app = Flask(__name__)
app.config['SECRET_KEY']=os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=7)


from src import debug, login, register

app.config['SERVER_NAME'] = 'agileffy.info'

app.run(
    host='0.0.0.0',
    port=443,
    debug=True,
    ssl_context=('your_path/XXXX.pem', 'your_path/XXXX.key'))


