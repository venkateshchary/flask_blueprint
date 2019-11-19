from flask import Flask, render_template, request


from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] ='HHSHDHSDH'

from bluep.modulo1 import modulo1_blueprint
from bluep.modulo2 import modulo2_blueprint
app.register_blueprint(modulo1_blueprint)
app.register_blueprint(modulo2_blueprint)