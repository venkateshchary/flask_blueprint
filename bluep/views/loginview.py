from flask import Blueprint,request,redirect
from bluep.headers import *
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
login_blueprint = Blueprint(name='login', import_name=__name__)

@login_blueprint.route('/login', methods=['POST'])
def login():
    print(app.config['SECRET_KEY'])
    return 'login view'