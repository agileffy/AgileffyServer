from src import app
from flask import make_response

@app.route('/debug')
def debugPage():
    return 'Hello World!'
