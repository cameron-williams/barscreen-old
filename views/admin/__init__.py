from flask import (
    Blueprint, render_template
)


admin = Blueprint('admin', __name__, static_folder='../../static')


@admin.route("/")
def index():
    return render_template("admin/admin.html")

@admin.route("/user")
def user():
    return render_template("admin/user.html")

@admin.route("/channels")
def channels():
    return render_template("admin/channels.html")

@admin.route("/addchannel")
def addchannel():
    form = NewchannelForm()
    if request.method == "POST" and form.validate_on_submit():
        channel = Channels(
            channel_name=form.channel_name.data,
            category=form.category.data,
            description=form.description.data,
            channel_img=form.channel_img.data,
        )
        db.session.add(channel)
        db.session.commit()
        flash("Successfully completed.")
    return render_template("admin/addchannel.html", form=form)
