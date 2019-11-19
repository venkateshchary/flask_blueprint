from flask import Blueprint
from bluep.headers import *
modulo1_blueprint = Blueprint(name='modulo1', import_name=__name__)


@modulo1_blueprint.route('/', methods=['GET'])
def index():
    print(app.config['SECRET_KEY'])
    app.logger.error('An error occurred')
    app.logger.info('request hit the api module1')
    return 'modulo1'