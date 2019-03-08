from flask import Blueprint, render_template

base = Blueprint('base', __name__, static_folder='../static')


@base.route("/")
def index():
    return render_template("index.html")


@base.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@base.route("/contact", methods=["POST","GET"])
def contact():
    return render_template("contact.html")


@base.route("/signup", methods=["POST","GET"])
def signup():
    return render_template("signup.html")