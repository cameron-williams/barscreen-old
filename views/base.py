from flask import Blueprint, render_template, request
from forms.contact import ContactForm
from services.google import Gmail

base = Blueprint('base', __name__, static_folder='../static')


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
        g.send_email(to="info@barscreen.tv", subject="New Contact Submission", body=msg)

    return render_template("contact.html", form=form)


@base.route("/signup", methods=["POST", "GET"])
def signup():
    return render_template("signup.html")
