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
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_swagger_ui import get_swaggerui_blueprint



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
app.config['JWT_TOKEN_LOCATION'] = ['headers']


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static',path)


# swagger configuration
SWAGGER_URL = '/api/docs' # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://petstore.swagger.io/v2/swagger.json' # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
SWAGGER_URL, # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
API_URL,
config={ # Swagger UI config overrides
'app_name': "Test application"
},
# oauth_config={ # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
# 'clientId': "your-client-id",
# 'clientSecret': "your-client-secret-if-required",
# 'realm': "your-realms",
# 'appName': "your-app-name",
# 'scopeSeparator': " ",
# 'additionalQueryStringParams': {'test': "hello"}
# }
)

# Register blueprint at URL
# (URL must match the one given to factory function above)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


'''
SWAGGER_URL = '/swagger'
API_URL = "/static/swagger.json"
swaggerui_blueprint= get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name':'Seans-Python-Flask-REST-Boilerplate'
    }
)
app.register_blueprint(swaggerui_blueprint,url_prefix=SWAGGER_URL)
'''


app.config["MONGO_URI"] = "mongodb://localhost:27017/flaskdb"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
salt = "venkatesh"



random_bytes = urandom(64)
secret_key = b64encode(random_bytes).decode('utf-8')
app.config['SECRET_KEY'] = secret_key

# Enable blacklisting and specify what kind of tokens to check
# against the blacklist
app.config['JWT_SECRET_KEY'] = secret_key  # Change this!
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)
blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    app.logger.info("jti %s"%jti)
    app.logger.info(blacklist)
    return jti in blacklist


from bluep.modulo1 import modulo1_blueprint
from bluep.modulo2 import modulo2_blueprint
from bluep.views.loginview import login_blueprint
app.register_blueprint(modulo1_blueprint)
app.register_blueprint(modulo2_blueprint)
app.register_blueprint(login_blueprint)