from flask import Flask, render_template, request
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
from base64 import b64encode
from os import urandom
import logging
from logging.handlers import RotatingFileHandler
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)

random_bytes = urandom(64)
secret_key = b64encode(random_bytes).decode('utf-8')
app.config['SECRET_KEY'] = secret_key

# Enable blacklisting and specify what kind of tokens to check
# against the blacklist
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

from bluep.modulo1 import modulo1_blueprint
from bluep.modulo2 import modulo2_blueprint
from bluep.views.loginview import login_blueprint
app.register_blueprint(modulo1_blueprint)
app.register_blueprint(modulo2_blueprint)
app.register_blueprint(login_blueprint)