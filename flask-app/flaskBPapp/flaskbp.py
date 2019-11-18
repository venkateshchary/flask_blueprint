from flask import Blueprint, render_template

dashboard = Blueprint('flask',__name__)

@dashboard.route("/")
def index():
    data = {"number":list(range(1990,2019))}
    return render_template('index.html',data=data)