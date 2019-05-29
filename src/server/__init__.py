from flask import Flask, request

server = Flask(__name__)
server.debug = True

from server import routes