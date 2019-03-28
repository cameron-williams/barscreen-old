"""
Barscreen Web App
"""

from flask import Flask, render_template, request, abort, jsonify, copy_current_request_context, redirect, url_for
from models import db, Users
from flask_login import LoginManager, login_required, login_user, current_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

login_manager = LoginManager()
bcrypt = Bcrypt()

LOCAL = False
if __name__ == "__main__":
    LOCAL = True


# Todo move secrets to env variables
def create_app():
    app = Flask(__name__, subdomain_matching=True)
    DB_URL = "postgresql+psycopg2://postgres:abdER422sh1@35.197.9.48:5432/barscreen"
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': DB_URL,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': "97e5782c0ef1621d168ed4229ac95f148d1d09a9abaa490d7349d363f16cc7b3",
        'SECURITY_PASSWORD_SALT': '86343d47f9f472d4d992a87faf8e831e83e3a6659bea49d2bed48dd6f0b4e1be',
    })
    if not LOCAL:
        app.config['SERVER_NAME'] = 'barscreen.tv'

    db.init_app(app)
    migrate = Migrate(app, db)
    bcrypt.init_app(app)
    bootstrap = Bootstrap(app)
    login_manager.init_app(app)
    login_manager.login_view = "dashboard.login"

    # register blueprints
    subdomain_routing = not LOCAL  # change this to false if you're testing locally
    from views import base
    from views.dashboard import dashboard
    from views.admin import admin

    app.register_blueprint(base.base)
    app.register_blueprint(admin, url_prefix="/ad" if LOCAL else None, subdomain="admin" if subdomain_routing else None)
    app.register_blueprint(dashboard, url_prefix="/dash" if LOCAL else None,
                           subdomain="dashboard" if subdomain_routing else None)
    return app


app = create_app()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("dashboard.login"))


if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)
