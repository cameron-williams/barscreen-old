import re
from os import urandom
from binascii import hexlify
import random
from functools import wraps
from flask import (
    Blueprint, request, redirect, url_for, abort, jsonify, g
)
from models import db, Loop, Show, Clip, Promo, shortFormVideoSchema, Users
from helpers import verify_password, confirm_token

roku = Blueprint('roku', __name__, static_folder='../../static')


def to_shortform_spec(media):
    """ Turns a clip into a shortform object for the roku json spec """
    _body = shortFormVideoSchema.copy()
    _body["id"] = "{}{}{}".format(media.id, type(
        media) == Clip and 'clip' or 'promo', hexlify(urandom(5)))
    _body["title"] = media.name
    _body["content"] = media.clip_url
    _body["thumbnail"] = "filler"
    _body["shortDescription"] = media.description
    return _body


@roku.route("/login", methods=["POST"])
def login():
    req = request.get_json()
    if not req:
        abort(400, "Post data can not be empty.")
    if not req.get("email") or not req.get("password"):
        abort(400, "Missing fields. Post data must include an email and password field.")
    # try and match user off given email
    matched_user = Users.query.filter_by(email=req["email"]).first()
    # double check password matches hash
    if not verify_password(matched_user.password, req["password"]):
        abort(401, "invalid credentials")
    if not matched_user.api_key:
        matched_user.api_key = hexlify(urandom(32))
        db.session.commit()
    return jsonify({"status": "success", "api_key": matched_user.api_key})


@roku.route("/get_loops", methods=["GET"])
def get_loops():
    api_key = request.args.get("api_key")
    current_user = db.session.query(Users).filter(
        Users.api_key == api_key).first()
    if not api_key or not current_user:
        abort(404)
    loops = [
        {"name": loop.name, "image_url": loop.image_url, "id": loop.id}
        for loop in db.session.query(Loop).filter(Loop.user_id == current_user.id).all()
    ]
    return jsonify({"status": "success", "loops": loops})


@roku.route("/pubs/loops/<loop_id>")
def get_loop(loop_id):
    """ Takes the pub id/loop id and returns a json payload that matches the feed spec """
    api_key = request.args.get("api_key")
    current_user = db.session.query(Users).filter(
        Users.api_key == api_key).first()
    if not api_key or not current_user:
        abort(404)
    publisher_id = current_user.id
    # grab loop from db (or 404)
    loop = db.session.query(Loop).filter(
        Loop.id == loop_id, Loop.user_id == publisher_id).first()
    if not loop:
        abort(404)

    last_played = loop.get_last_played_clips()

    # copy the json schema to make adjustments to
    json_feed = {
        "providerName": "BarscreenTV",
        "lastUpdated": str,
        "language": "en",
        "movies": [],
        "series": [],
        "shortFormVideos": [],
        "tvSpecials": [],
        "playlists": []
    }
    json_feed["lastUpdated"] = loop.last_updated

    # iterate playlist and add clips as needed
    for i in loop.playlist:
        media_id = re.search(r'\d+', i).group()
        if 'promo' in i.lower():
            promo = db.session.query(Promo).filter(
                Promo.id == media_id).first()
            # if promo
            if not promo:
                continue
            # add promo to json feed
            json_feed["shortFormVideos"].append(to_shortform_spec(promo))
        else:
            show = Show.query.filter_by(id=media_id).first()
            # more in depth, add clip from show based on settings
            clip_selection = db.session.query(Clip).filter(
                Clip.show_id == show.id).order_by(Clip.id.desc()).all()[:show.lookback]
            clip = None

            # skip if no clips
            if not clip_selection:
                continue

            # handle only 1 clip on show
            if len(clip_selection) == 1:
                clip = clip_selection.pop()
            else:
                # clip id that was last played for this show
                last_clip_id = last_played.get(show.id)
                # handle random show clip selection
                if show.order == 'random':
                    if last_clip_id and last_clip_id in clip:
                        clip_selection.pop(clip_selection.index(last_clip_id))
                    clip = random.choice(clip_selection)

                # handle recent show clip selection
                else:
                    # if no last played clip, play most recent
                    if not last_clip_id:
                        clip = clip_selection[0]
                    else:
                        # get next clip in selection based off last played clip id (or start at overflow to start)
                        try:
                            clip = clip_selection[[c.id for c in clip_selection].index(
                                last_clip_id)+1]
                        except IndexError:
                            clip = clip_selection[0]

            # set last played clip for current show to currently selected clip
            last_played[show.id] = clip.id
            loop.set_last_played_clips(last_played)
            db.session.commit()
            json_feed["shortFormVideos"].append(to_shortform_spec(clip))
    # add playlist for current shortFormVideos
    playlist = {
        "name": loop.name,
        "itemIds": [i["id"] for i in json_feed["shortFormVideos"]]
    }
    json_feed["playlists"].append(playlist)
    # return json_feed as json
    return jsonify(json_feed)
