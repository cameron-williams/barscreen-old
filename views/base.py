from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from forms.contact import ContactForm
from forms.signup import SignupForm
from services.google_clients import Gmail
from models import Users, db
from sqlalchemy.exc import IntegrityError
from functools import wraps

base = Blueprint('base', __name__, static_folder='../static')


def requires_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.admin:
            flash("Invalid user permissions.")
            return redirect(url_for('dashboard.login'))
        return f(*args, **kwargs)
    return wrapper


@base.route("/")
def index():
    return render_template("index.html")

@base.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@base.route("/features", methods=["GET"])
def features():
    return render_template("features.html")

@base.route("/contact", methods=["POST", "GET"])
def contact():
    form = ContactForm()
    if request.method == "POST" and form.validate_on_submit():
        g = Gmail(delegated_user="cam@barscreen.tv")
        msg = """
            New Contact Form Submission:
            Name: {}
            Email: {}
            Message: {}""".format(
            form.name.data,
            form.email.data,
            form.message.data,
        )
        g.send_email(to="info@barscreen.tv",
                     subject="New Contact Submission", body=msg)

    return render_template("contact.html", form=form)


@base.route("/signup", methods=["POST", "GET"])
def signup():
    form = SignupForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            user = Users(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                phone_number=form.phone.data,
                email=form.email.data,
                company=form.company.data,
            )
            db.session.add(user)
            db.session.commit()
            g = Gmail(delegated_user="cam@barscreen.tv")
            msg = """
                New Sign Up:
                First Name: {}
                Last Name: {}
                Email: {}
                Phone Number: {}
                Company: {}""".format(
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                form.phone.data,
                form.company.data,
            )
            g.send_email(to="info@barscreen.tv",
                         subject="New Sign Up", body=msg)
        except IntegrityError:
            flash("Sorry, a user with that email exists already.", category="error")
        except Exception:
            flash("Unknown error has occurred. Please try again.", category="error")
        flash("Your account is pending, if you are approved we will be in touch with your credentials. Please check email your email.", category="success")
    return render_template("signup.html", form=form)
