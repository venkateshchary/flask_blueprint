from flask import Blueprint
from bluep.headers import *
modulo1_blueprint = Blueprint(name='modulo1', import_name=__name__)


@modulo1_blueprint.route('/', methods=['GET'])
def index():
    print(app.config['SECRET_KEY'])
    return 'modulo1'