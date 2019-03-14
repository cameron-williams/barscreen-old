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

@dashboard.route("/password")
def password():
    return render_template("dashboard/password.html")

@dashboard.route("/loops")
def loops():
    return render_template("dashboard/loops.html")

@dashboard.route("/create")
def create():
    return render_template("dashboard/create.html")
