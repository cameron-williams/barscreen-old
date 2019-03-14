from flask import (
    Blueprint, render_template, request, flash, redirect, url_for
)
from flask_login import login_required, login_user
from forms.login import LoginForm
from models import Users

dashboard = Blueprint('dashboard', __name__, static_folder='../../static')


@login_required
@dashboard.route("/")
def index():
    return render_template("dashboard/dashboard.html")


@dashboard.route("/index")
def alt_index():
    return render_template("dashboard/dashboard.html")


@dashboard.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        matched_user = Users.query.filter_by(email=form.email.data).first()
        if matched_user:
            login_user(matched_user)
            return redirect(url_for("dashboard.alt_index"))
        else:
            flash("User not found", "error")
    return render_template("dashboard/login.html", form=form)


@login_required
@dashboard.route("/password")
def password():
    return render_template("dashboard/password.html")


@login_required
@dashboard.route("/loops")
def loops():
    return render_template("dashboard/loops.html")


@login_required
@dashboard.route("/create")
def create():
    return render_template("dashboard/create.html")

@dashboard.route("/account")
def account():
    return render_template("dashboard/account.html")
