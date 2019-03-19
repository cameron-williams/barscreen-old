from flask import (
    Blueprint, render_template, request, jsonify, abort, flash, url_for, redirect
)
from flask_login import login_required
from forms.password import CreatePassword
from models import db, Users
from helpers import generate_confirmation_token, confirm_token
from services.google import Gmail

admin = Blueprint('admin', __name__, static_folder='../../static')


@admin.route("/")
@login_required
def index():
    users = Users.query.all()
    return render_template("admin/admin.html", users=users)

@admin.route("/approve_user", methods=["POST"])
def approve_user():
    req = request.get_json()
    existing_user = Users.query.filter_by(email=req["email"]).first()
    if existing_user.confirmed:
        abort(400, "User is confirmed already.")

    # create gmail client
    gmail = Gmail(delegated_user="info@barscreen.tv")
    # generate password token
    password_token = generate_confirmation_token(existing_user.email)
    
    # Fill in email body and send email
    email_body = """Hi there, please visit the link below to create a password: {}""".format(
        url_for('admin.confirm_email', token=password_token),   
    )
    gmail.send_email(to=existing_user.email, subject="New Password Token", body=email_body)
    return jsonify({"success": True})


@admin.route("/confirm/<token>", methods=["GET", "POST"])
def confirm_email(token):
    # make sure token is set based off what type of request we're getting
    if token:
        form = CreatePassword(token=token)
    else:
        form = CreatePassword()
    if not token:
        token = form.token.data
    # try and confirm token, abort to signup if invalid or expired
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', category='danger')
        return redirect(url_for('base.signup'))

    # pull user associated with token
    user = Users.query.filter_by(email=email).first()
    if not user:
        abort(400, 'Invalid token.')
    if user.confirmed:
        flash('Account already confirmed. Please log in.', category="success")
        return redirect(url_for('dashboard.login'))
    
    # if form submit, add new password to user and redirect them to dashboard
    if request.method == "POST" and form.validate_on_submit():
        user.set_password(form.password.data)
        user.confirmed = True
        db.session.commit()
        flash("Password set successfully.", category="success")
        return redirect(url_for('dashboard.index'))
    return render_template("admin/create_password.html", form=form, token=token)

@admin.route("/user")
@login_required
def user():
    return render_template("admin/user.html")
