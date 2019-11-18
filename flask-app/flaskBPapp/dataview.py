from flask import Blueprint, render_template

data = Blueprint('dataview', __name__)


@data.route("/")
def index():
    data = {"number": 8989}
    return render_template('index.html', data=data)
