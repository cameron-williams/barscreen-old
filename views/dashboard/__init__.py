from flask import (
    Blueprint, render_template, request, flash, jsonify, redirect, url_for, abort, json, make_response
)
from flask_login import login_required, login_user, current_user, logout_user
from forms.login import LoginForm
from forms.password import CreatePassword
from forms.dash_newpromo import DashNewPromoForm
from models import Users, db, Channel, Show, Clip, Promo, Loop
from services.imaging import screencap_from_video
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
from services.google_clients import Gmail, GoogleStorage
from helpers import verify_password, confirm_token, generate_confirmation_token, InvalidTokenError
import re
import logging
from flask import current_app as app
from datetime import timedelta
from functools import update_wrapper


dashboard = Blueprint('dashboard', __name__, static_folder='../../static')


def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
    """
    Decorator that adds support for CORS to a route.

    origin: Access-Control-Allow-Origin
    methods: Access-Control-Allow-Methods
    headers: Access-Control-Allow-Headers
    max_age: Access-Control-Max-Age
    attach_to_all: Attach CORS headers to responses for all methods
    automatic_options: Handle OPTIONS pre-flight response
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers

            # Cancel Strict-Transport-Security if still enabled
            h['Strict-Transport-Security'] = 'max-age=0'

            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


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
        matched_user = db.session.query(Users).filter(
            Users.email == form.email.data).first()
        if not matched_user:
            flash("Invalid email or password.", "error")
            return redirect(url_for("dashboard.index"))
        if not matched_user.confirmed:
            flash("User account has not been approved yet.", "error")
            return redirect(url_for("dashboard.index"))
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
    except InvalidTokenError:
        flash('The confirmation link is invalid or has expired.', category='danger')
        return redirect(url_for('base.signup'))

    # pull user associated with token
    user = Users.query.filter_by(email=email).first()
    if not user:
        abort(400, 'Invalid token.')

    # if form submit, add new password to user and redirect them to dashboard
    if request.method == "POST" and form.validate_on_submit():
        user.set_password(form.password.data)
        user.confirmed = True
        db.session.commit()
        flash("Password set successfully.", category="success")
        return redirect(url_for('dashboard.index'))
    return render_template("dashboard/password.html", form=form, token=token)


@dashboard.route("/change_password", methods=["POST"])
def change_password():
    req = request.get_json()
    existing_user = Users.query.filter_by(email=req["email"]).first()
    # create gmail client
    gmail = Gmail(delegated_user="info@barscreen.tv")
    # generate password token
    password_token = generate_confirmation_token(existing_user.email)

    # Fill in email body and send email
    email_body = """Please click on the link to reset your BarScreen password. Link: {}""".format(
        url_for('dashboard.confirm_email', token=password_token),
    )
    gmail.send_email(to=existing_user.email,
                     subject="BarScreen Account", body=email_body)
    return jsonify({"success": True})


@dashboard.route("/loops")
@login_required
def loops():
    return render_template("dashboard/loops.html")


@dashboard.route("/loops/addloop", methods=["POST", "GET"])
@login_required
def addloop():
    error = None
    trends = Channel.query.order_by(Channel.id.desc()).limit(10).all()
    entertainments = Channel.query.order_by(Channel.id.desc()).filter(
        (Channel.category).like('Entertainment')).all()
    sports = Channel.query.order_by(Channel.id.desc()).filter(
        (Channel.category).like('Sports')).all()
    news = Channel.query.order_by(Channel.id.desc()).filter(
        (Channel.category).like('News')).all()
    form = DashNewPromoForm()
    if request.method == "POST" and form.validate_on_submit():
        storage = GoogleStorage()
        print("ya")
        try:
            # Get secure filename from file data.
            fn = secure_filename(form.promo_file.data.filename)
            # Save file locally.
            form.promo_file.data.save('/tmp/' + fn)
            # Get frame from 5 seconds into video and save it locally.
            image_path = screencap_from_video("/tmp/{}".format(fn))

            # save video locally
            url = storage.upload_promo_video(
                name=fn, file=open("/tmp/"+fn))

            screencap_url = storage.upload_promo_image(
                name=image_path.split("/")[-1], image_data=open(image_path).read())

            current_user.promos.append(Promo(
                name=form.promo_name.data,
                description=form.description.data,
                clip_url=url,
                image_url=screencap_url,
            ))

            db.session.commit()
            flash("Promo created successfully.", category="success")

        except Exception as err:
            print(err)
            logging.error(
                "error uploading new loop: {} {}".format(type(err), err))
            flash(
                "Error creating new loop. Please try again in a few minutes", category="error")
    return render_template("dashboard/addloop.html", form=form, error=error, current_user=current_user, trends=trends, entertainments=entertainments, sports=sports, news=news)


@dashboard.route("/submit_loop", methods=["POST", "PUT"])
@login_required
def submit_loop():
    req = request.get_json()
    current_user = Users.query.filter_by(id=req["user_id"]).first()
    image_url = None
    if req.get("image_data"):
        # write file locally
        with open("/tmp/uploaded_image.png", "wb") as f:
            f.write(req["image_data"].split(",")[-1].decode("base64"))
        # upload file to cdn
        storage = GoogleStorage()
        image_url = storage.upload_loop_image(
            req["name"] + ".png", open("/tmp/uploaded_image.png").read())
    if request.method == "POST":
        # write file locally
        try:
            current_user.loops.append(Loop(
                name=req["name"],
                playlist=req["playlist"],
                image_url=image_url
            ))
            db.session.commit()
        except Exception as err:
            abort(400, err)
    if request.method == "PUT":
        loop = Loop.query.filter_by(id=req["loop_id"]).first()
        if req["name"] != loop.name:
            loop.name = req["name"]
        if req["playlist"] != loop.playlist:
            loop.playlist = req["playlist"]
        if image_url and image_url != loop.image_url:
            loop.image_url = image_url
        db.session.commit()
    return jsonify({"success": True})


@dashboard.route("/loops/<loop_id>")
@login_required
def editloop(loop_id):
    trends = Channel.query.order_by(Channel.id.desc()).limit(10).all()
    entertainments = Channel.query.order_by(Channel.id.desc()).filter(
        (Channel.category).like('Entertainment')).all()
    sports = Channel.query.order_by(Channel.id.desc()).filter(
        (Channel.category).like('Sports')).all()
    news = Channel.query.order_by(Channel.id.desc()).filter(
        (Channel.category).like('News')).all()
    loop_playlist = []
    current_loop = Loop.query.filter_by(id=loop_id).first()
    form = DashNewPromoForm()
    if not current_loop:
        abort(404, {"error": "No channel by that id. (id:{})".format(loop_id)})
    for i in current_loop.playlist:
        media_id = re.search(r'\d+', i).group()
        if 'promo' in i.lower():
            promo = db.session.query(Promo).filter(
                Promo.id == media_id).first()
            # if promo
            if not promo:
                continue
            loop_playlist.append(
                {'id': promo.id, 'name': promo.name, 'image_url': promo.image_url, 'type': 'promo'})
        else:
            show = Show.query.filter_by(id=media_id).first()
            loop_playlist.append({'id': show.id, 'name': show.name,
                                  'image_url': show.clips[-1].image_url, 'type': 'show'})
        print(json.dumps(loop_playlist))
    return render_template("dashboard/editloop.html", form=form, loop_playlist=json.dumps(loop_playlist), current_loop=current_loop, current_user=current_user, trends=trends, entertainments=entertainments, sports=sports, news=news)


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


@dashboard.route("/editprofile", methods=["POST"])
@login_required
def editprofile():
    req = request.get_json()
    user = Users.query.filter_by(id=req["user_id"]).first()
    if request.method == "POST":
        if req["first_name"] != user.first_name:
            user.first_name = req["first_name"]
        if req["last_name"] != user.last_name:
            user.last_name = req["last_name"]
        if req["phone_number"] != user.phone_number:
            user.phone_number = req["phone_number"]
        db.session.commit()
    return jsonify({"success": True})


@dashboard.route("/editemail", methods=["POST"])
@login_required
def editemail():
    req = request.get_json()
    user = Users.query.filter_by(id=req["user_id"]).first()
    if request.method == "POST":
        if req["email"] != user.email:
            user.email = req["email"]
        db.session.commit()
    return jsonify({"success": True})


@dashboard.route("/channel")
@login_required
def channel():
    return render_template("dashboard/channel.html")


@dashboard.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard.login'))
