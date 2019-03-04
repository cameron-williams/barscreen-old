"""
Barscreen Web App
"""

from flask import Flask, render_template, request, abort, jsonify, copy_current_request_context
from models import db, User
from flask_login import LoginManager, login_required, login_user, current_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from sqlalchemy.sql.expression import func
from flask_bootstrap import Bootstrap

login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    DB_URL = "postgresql+psycopg2://cam:root@localhost:5432/barscreen"
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': DB_URL,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': "97e5782c0ef1621d168ed4229ac95f148d1d09a9abaa490d7349d363f16cc7b3"
    })
    db.init_app(app)
    migrate = Migrate(app, db)
    bcrypt.init_app(app)
    bootstrap = Bootstrap(app)
    login_manager.init_app(app)
    return app


app = create_app()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")


@app.route("/loops", methods=["POST", "GET"])
def loops():
    return render_template("loops.html")


@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html")

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/contact", methods=["POST","GET"])
def contact():
    return render_template("contact.html")

@app.route("/signup", methods=["POST","GET"])
def signup():
    return render_template("signup.html")

if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)
