from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from forms.contact import ContactForm
from forms.signup import SignupForm
from services.google import Gmail
from models import Users, db
from sqlalchemy.exc import IntegrityError
from functools import wraps

base = Blueprint('base', __name__, static_folder='../static')


def requires_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.admin:
            print("invalid user permissions")
            flash("Invalid user permissions.")
            return redirect(url_for('dashboard.login'))
        print("valid user permissions")
        return f(*args, **kwargs)
    return wrapper


@base.route("/")
def index():
    return render_template("index.html")


@base.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


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
        except IntegrityError:
            flash("Sorry, a user with that email exists already.", category="error")
        except Exception:
            flash("Unknown error has occored. Please try again.", category="error")
        flash("Thanks, we will be in touch shortly.", category="success")
    return render_template("signup.html", form=form)
