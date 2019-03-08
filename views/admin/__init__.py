from flask import (
    Blueprint, render_template
)


admin = Blueprint('admin', __name__, static_folder='../../static')


@admin.route("/")
def index():
    return "there will be an admin page here eventually"
