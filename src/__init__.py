import os
from datetime import timedelta

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

from src import debug, login, register

app.run(
    host='0.0.0.0',
    port=5000,
    debug=True)
