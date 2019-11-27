from flask import Blueprint,request,redirect,jsonify
import hashlib
from bluep.headers import *
import datetime
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
login_blueprint = Blueprint(name='user', import_name=__name__)

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.

@login_blueprint.route('/home',methods=['POST','GET'])
def home():
    return 'home page is loaded'

def password_generate(psw):
    pw_hash =  psw+ salt
    h = hashlib.md5(pw_hash.encode())
    pw_hash = h.hexdigest()
    app.logger.info("enterd password: %s | hash generated: %s"%(psw,pw_hash))
    return pw_hash

@login_blueprint.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    user = mongo.db.users.find_one_or_404({"username":username,"password":password_generate(password)})
    expires = datetime.timedelta(minutes=5)
    ret = {
        'access_token': create_access_token(identity=username,expires_delta=expires),
        'refresh_token': create_refresh_token(identity=username)
    }
    return jsonify(ret), 200


@login_blueprint.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    online_users = mongo.db.users.find({"username": username}).limit(1)
    result =None; msg=None
    for i in online_users:
        result=i
    if result ==None:
        online_user = mongo.db.users.insert({"username": username,"password":password_generate(password)})
        app.logger.info("user is inserted: %s"%online_user)
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token,message='created'), 200
    else:
        app.logger.error("==========>user name is already present")
        msg="user already exist"
        return jsonify(message=msg), 200


@login_blueprint.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

#@jwt.token_in_blacklist_loader
#def check_token_in_blacklist(token_dict: dict) -> bool:

@login_blueprint.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


@login_blueprint.route('/userdelete/<string:username>',methods=['DELETE'])
def delete_user(username):
    username_from_body = request.json.get('username', None)
    app.logger.info(username)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    d = mongo.db.users.find({"username":username}).limit(1)
    result = None
    for i in d:
        result= i
    if result !=None:
        d_user = mongo.db.users.remove({"username":username})
        app.logger.info("deleted user is :%s"%d_user)
        return jsonify({"message":"user is deleted "}),200
    return jsonify({"message":"no user found with the username"}),200