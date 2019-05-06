from io import BytesIO

from flask import (
    Blueprint, render_template, request, jsonify, abort, flash, url_for, redirect
)
from views.base import requires_admin
from sqlalchemy.exc import IntegrityError
from forms.newchannel import NewchannelForm
from forms.newshow import NewShowForm
from forms.newpromo import NewPromoForm
from forms.newclip import NewClipForm
from flask_login import login_required, logout_user
from forms.password import CreatePassword
from models import db, Users, Channel, Show, Clip, Promo, Loop
from helpers import generate_confirmation_token, confirm_token
from services.google_clients import Gmail, GoogleStorage
from PIL import Image
from urllib import unquote_plus
from base64 import b64encode
from werkzeug.utils import secure_filename

admin = Blueprint('admin', __name__, static_folder='../../static')


@admin.route("/")
@login_required
@requires_admin
def index():
    users = Users.query.all()
    return render_template("admin/admin.html", users=users)


@admin.route("/approve_user", methods=["POST"])
@login_required
@requires_admin
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
    email_body = """Congratulations you have been approved for a Barscreen account! Below is a link to create a password. Your email will be used for your username. Link: {}""".format(
        url_for('dashboard.confirm_email', token=password_token),
    )
    gmail.send_email(to=existing_user.email,
                     subject="BarScreen Account", body=email_body)
    return jsonify({"success": True})


@admin.route("/confirm/<token>", methods=["GET", "POST"])
@login_required
@requires_admin
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


@admin.route("/user/<user_id>", methods=["GET", "POST"])
@login_required
@requires_admin
def user(user_id):
    current_user = Users.query.filter_by(id=user_id).first()
    if not current_user:
        abort(404, {"error": "User not found"})
    if request.method == 'POST':
        data = {unquote_plus(k.split("=")[0]): unquote_plus(
            k.split("=")[1]) for k in request.get_data().split("&")}
        if data["name"] in ('confirmed', 'ads'):
            if data['value'].lower() == 'false':
                data['value'] = False
            else:
                data['value'] = True
        setattr(current_user, data["name"], data["value"])
        db.session.commit()
        return ''
    return render_template("admin/user.html", current_user=current_user)


@admin.route("/user/<user_id>/<promo_id>", methods=["GET", "POST"])
@login_required
@requires_admin
def promoid(user_id, promo_id):
    """ Specific channel route, allows edits to specified channel. """
    current_promo = Promo.query.filter_by(
        user_id=user_id, id=promo_id).first()
    if not current_promo:
        abort(404, {"error": "No clip by that id. (id:{})".format(show_id)})
    return render_template("admin/promoid.html", current_promo=current_promo, user_id=user_id)


@admin.route("/user/<user_id>/addpromo", methods=["POST", "GET"])
@login_required
@requires_admin
def addpromo(user_id):
    """ Add Promo route. Adds clip to whatever the current show that is being edited. """
    error = None
    current_user = Users.query.filter_by(id=user_id).first()
    form = NewPromoForm()
    if request.method == "POST" and form.validate_on_submit():
        storage = GoogleStorage()
        try:
            current_user = Users.query.filter_by(id=user_id).first()
            url = storage.upload_promo_video(name=secure_filename(form.clip_file.data.filename), file=form.clip_file.data)
            current_user.promos.append(Promo(
                name=form.promo_name.data,
                description=form.description.data,
                clip_url=url
            ))
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if 'duplicate key value violates unique constraint' in str(e):
                error = 'show name already registered.'
        flash("Promo Created.", category="success")
    return render_template("admin/addpromo.html", form=form, error=error, current_user=current_user)


@admin.route("/user/<user_id>/addloop")
@login_required
@requires_admin
def addloop(user_id):
    current_user = Users.query.filter_by(id=user_id).first()
    shows = Show.query.all()
    promos = Promo.query.filter_by(user_id=user_id).all()
    return render_template("admin/addloop.html", current_user=current_user, shows=shows, promos=promos)


@admin.route("/submit_loop", methods=["POST"])
@login_required
@requires_admin
def submit_loop():
    req = request.get_json()
    current_user = Users.query.filter_by(id=req["user_id"]).first()
    if request.method == "POST":
        try:
            current_user.loops.append(Loop(
                name=req["name"],
                playlist=req["playlist"]
            ))
            db.session.commit()
        except Exception as err:
            print(err)
            abort(400, err)
    return jsonify({"success": True})


@admin.route("/channels")
@login_required
@requires_admin
def channels():
    """ Route for viewing all channels """
    channels = Channel.query.all()
    return render_template("admin/channels.html", channels=channels)


@admin.route("/channels/<channel_id>", methods=["GET", "POST"])
@login_required
@requires_admin
def channelid(channel_id):
    """ Specific channel route, allows edits to specified channel. """
    current_channel = Channel.query.filter_by(id=channel_id).first()
    if not current_channel:
        abort(404, {"error": "No channel by that id. (id:{})".format(channel_id)})
    return render_template("admin/channelid.html", current_channel=current_channel)


@admin.route("/channels/<channel_id>/<show_id>", methods=["GET", "POST"])
@login_required
@requires_admin
def showid(channel_id, show_id):
    """ Specific channel route, allows edits to specified channel. """
    current_show = Show.query.filter_by(
        channel_id=channel_id, id=show_id).first()
    if not current_show:
        abort(404, {"error": "No show by that id. (id:{})".format(show_id)})
    return render_template("admin/showid.html", current_show=current_show, channel_id=channel_id)


@admin.route("/channels/<channel_id>/<show_id>/<clip_id>", methods=["GET", "POST"])
@login_required
@requires_admin
def clipid(channel_id, show_id, clip_id):
    """ Specific channel route, allows edits to specified channel. """
    current_clip = Clip.query.filter_by(
        show_id=show_id, id=clip_id).first()
    if not current_clip:
        abort(404, {"error": "No clip by that id. (id:{})".format(show_id)})
    return render_template("admin/clipid.html", current_clip=current_clip, show_id=show_id, channel_id=channel_id)


@admin.route("/channels/<channel_id>/<show_id>/addclip", methods=["POST", "GET"])
@login_required
@requires_admin
def addclip(channel_id, show_id):
    """ Add Clip route. Adds clip to whatever the current show that is being edited. """
    error = None
    form = NewClipForm()
    if request.method == "POST" and form.validate_on_submit():
        storage = GoogleStorage()
        try:
            current_show = Show.query.filter_by(
                channel_id=channel_id, id=show_id).first()
            # upload video to storage and save url
            url = storage.upload_clip_video(name=secure_filename(form.clip_file.data.filename), file=form.clip_file.data)
            current_show.clips.append(Clip(
                name=form.clip_name.data,
                description=form.description.data,
                clip_url=url
            ))
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if 'duplicate key value violates unique constraint' in str(e):
                error = 'show name already registered.'
        flash("Clip Created.", category="success")
    return render_template("admin/addclip.html", form=form, error=error)


@admin.route("/channels/<channel_id>/addshow", methods=["POST", "GET"])
@login_required
@requires_admin
def addshow(channel_id):
    """ Add Show route. Adds show to whatever the current channel that is being edited. """
    error = None
    form = NewShowForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            current_channel = Channel.query.filter_by(id=channel_id).first()
            current_channel.shows.append(Show(
                name=form.show_name.data,
                description=form.description.data,
                lookback=int(form.lookback.data),
                order=form.order.data
            ))
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            if 'duplicate key value violates unique constraint' in str(e):
                error = 'show name already registered.'
        flash("Show Created.", category="success")
    return render_template("admin/addshow.html", form=form, error=error)


@admin.route("/addchannel", methods=["POST", "GET"])
@login_required
@requires_admin
def addchannel():
    form = NewchannelForm()
    error = None

    if request.method == "POST" and form.validate_on_submit():
        storage = GoogleStorage()
        image_file = form.channel_img.data
        image_data = image_file.read()
        image_bytes = BytesIO(image_data)
        img = Image.open(image_bytes)

        size = img.size
        width = size[0]
        height = size[1]

        if width != 540 and height != 405:
            error = 'invalid image size'
            print(error)
        else:
            try:
                url = storage.upload_channel_image(name=secure_filename(form.channel_img.data.filename), image_data=image_data)
                channel = Channel(
                    name=form.channel_name.data,
                    category=form.category.data,
                    description=form.description.data,
                    image_url=url
                )
                db.session.add(channel)

                db.session.commit()
                flash("Successfully completed.")

            except IntegrityError as e:
                db.session.rollback()
                if 'duplicate key value violates unique constraint' in str(e):
                    error = 'channel name already registered.'
                else:
                    error = 'failed to add channel.'
            except AssertionError as e:
                db.session.rollback()
                error = str(e)
    return render_template("admin/addchannel.html", form=form, error=error)


@admin.route("/clips")
@login_required
@requires_admin
def clips():
    clips = Clip.query.all()
    return render_template("admin/clips.html", clips=clips)


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard.login'))
