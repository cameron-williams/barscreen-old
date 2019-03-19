from flask import (
    Blueprint, render_template, request, flash, redirect, url_for
)
from flask_login import login_required, login_user, current_user
from forms.login import LoginForm
from models import Users
from helpers import verify_password

dashboard = Blueprint('dashboard', __name__, static_folder='../../static')


@dashboard.route("/")
@login_required
def index():
    return render_template("dashboard/dashboard.html")


@dashboard.route("/index")
@login_required
def alt_index():
    return render_template("dashboard/dashboard.html")


@dashboard.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        # try and match user off given email
        matched_user = Users.query.filter_by(email=form.email.data).first()
        # double check password matches hash
        if verify_password(matched_user.password, str(form.password.data)):
            login_user(matched_user)
            return redirect(url_for("dashboard.index"))
        else:
            flash("Invalid email or password.", "error")
    return render_template("dashboard/login.html", form=form)


@login_required
@dashboard.route("/password")
def password():
    return render_template("dashboard/password.html")


@dashboard.route("/loops")
@login_required
def loops():
    print(current_user)
    return render_template("dashboard/loops.html")


@dashboard.route("/create")
@login_required
def create():
    return render_template("dashboard/create.html")


@dashboard.route("/account")
@login_required
def account():
    return render_template("dashboard/account.html")


@dashboard.route("/channel")
def channel():
    return render_template("dashboard/channel.html")
