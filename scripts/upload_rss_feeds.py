"""
Script that takes all Armchair Tourist RSS feeds and uploads
them into our CDN/DB.
"""
from app import create_app
import os
import requests

from models import db, Show, Clip
from services.google_clients import GoogleStorage
from services.imaging import resize_image


def armchair_tourist_witw_feed():
    """>model
    Downloads and uploads the beaches feed from ArmchairTourist to our db.
    """
    g = GoogleStorage()
    feed_url = "http://www.armchairtourist.com/feed/feed.php"
    r = requests.get(feed_url)
    r.raise_for_status()
    show = db.session.query(Show).filter(
        Show.name == "Where in the World?").first()
    existing_clips = {clip.name: clip for clip in db.session.query(
        Clip).filter(Clip.show_id == show.id).all()}

    # Iterate each entry in the feed.
    for entry in r.json()["shortFormVideos"]:

        # Only continue if the entry does not exist as a clip already.
        if not existing_clips.get(entry["title"]):

            # Download thumbnail.
            image_req = requests.get(entry["thumbnail"], stream=True)
            image_url = None
            image_extension = None
            try:
                image_extension = entry["thumbnail"].split(
                    "/")[-1].split(".")[-1]
            except Exception as err:
                print(err)
            image_filename = entry["title"]+".{}".format(image_extension)
            image_path = "/tmp/{}".format(image_filename)
            if image_req.ok:
                with open(image_path, 'wb') as f:
                    for chunk in image_req:
                        if chunk:
                            f.write(chunk)
                            f.flush()
                resize_image(image_path)

                image_url = g.upload_clip_image(
                    entry["title"]+".{}".format(image_extension), open(image_path).read())

            # Download video.
            vid_url = entry["content"]["videos"][0]["url"]
            video_req = requests.get(vid_url, stream=True)
            if video_req.ok:
                file_extension = None
                try:
                    file_extension = vid_url.split("/")[-1].split(".")[-1]
                except Exception as err:
                    print(err)
                if not file_extension:
                    file_extension = ".mp4"
                file_path = "/tmp/{}.{}".format(entry["title"], file_extension)
                with open(file_path, 'wb') as f:
                    for chunk in video_req.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                # Upload clip video to google storage.
                video_url = g.upload_clip_video(
                    entry["title"]+".{}".format(file_extension), open(file_path))

            # We have downloaded/uploaded everything so now add to DB.
            new_clip = Clip()
            new_clip.name = entry["title"]
            new_clip.description = entry["shortDescription"]
            new_clip.duration = entry["content"]["duration"]
            new_clip.clip_url = video_url
            new_clip.image_url = image_url
            show.clips.append(new_clip)
            existing_clips[new_clip.name] = new_clip
            print("Added clip", new_clip.name)
            db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        armchair_tourist_witw_feed()
