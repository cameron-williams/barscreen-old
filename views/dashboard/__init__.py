from flask import (
    Blueprint, render_template
)


dashboard = Blueprint('dashboard', __name__, static_folder='../../static')


@dashboard.route("/")
def index():
    return render_template("dashboard/dashboard.html")


@dashboard.route("/login")
def login():
    return render_template("dashboard/login.html")
