from flask import (
    Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort
)
from flask_login import login_required, login_user, current_user, logout_user
from forms.login import LoginForm
from forms.password import CreatePassword
from models import Users, db, Channel, Show, Clip, Promo, Loop
from helpers import verify_password, confirm_token

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
            if matched_user.admin:
                return redirect(url_for("admin.index"))
            return redirect(url_for("dashboard.index"))
        else:
            flash("Invalid email or password.", "error")
    return render_template("dashboard/login.html", form=form)


@dashboard.route("/confirm/<token>", methods=["GET", "POST"])
@login_required
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
    return render_template("dashboard/password.html", form=form, token=token)


@dashboard.route("/loops")
@login_required
def loops():
    return render_template("dashboard/loops.html")


@dashboard.route("/loops/addloop")
@login_required
def addloop():
    trends = Channel.query.order_by(Channel.id.desc()).limit(10).all()
    entertainments = Channel.query.order_by(Channel.id.desc()).filter((Channel.category).like('Entertainment')).all()
    sports = Channel.query.order_by(Channel.id.desc()).filter((Channel.category).like('Sports')).all()
    news = Channel.query.order_by(Channel.id.desc()).filter((Channel.category).like('News')).all()
    return render_template("dashboard/addloop.html", current_user=current_user, trends=trends, entertainments=entertainments, sports=sports, news=news)

@dashboard.route("/loops/<loop_id>")
@login_required
def editloop(loop_id):
    trends = Channel.query.order_by(Channel.id.desc()).limit(10).all()
    entertainments = Channel.query.order_by(Channel.id.desc()).filter((Channel.category).like('Entertainment')).all()
    sports = Channel.query.order_by(Channel.id.desc()).filter((Channel.category).like('Sports')).all()
    news = Channel.query.order_by(Channel.id.desc()).filter((Channel.category).like('News')).all()
    current_loop = Loop.query.filter_by(id=loop_id).first()
    if not current_loop:
        abort(404, {"error": "No channel by that id. (id:{})".format(loop_id)})
    return render_template("dashboard/editloop.html", current_loop=current_loop, current_user=current_user, trends=trends, entertainments=entertainments, sports=sports, news=news)


@dashboard.route("/create/get_channel", methods=["POST"])
@login_required
def get_channel():
    req = request.get_json()
    current_channel = Channel.query.filter_by(id=req["channel_id"]).first()
    return jsonify({'data': render_template('dashboard/channelmod.html', current_channel=current_channel)})


@dashboard.route("/account")
@login_required
def account():
    return render_template("dashboard/account.html")


@dashboard.route("/channel")
@login_required
def channel():
    return render_template("dashboard/channel.html")


@dashboard.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard.login'))
