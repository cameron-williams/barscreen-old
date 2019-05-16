"""
Imaging Tools
"""
import os
import subprocess
import urllib2


try:
    if os.path.exists("/usr/bin/ffmpeg"):
        ffmpeg = "/usr/bin/ffmpeg"
    else:
        ffmpeg = subprocess.check_output(["which", "ffmpeg"]).replace("\n", "")
except subprocess.CalledProcessError:
    print("Error: FFMPEG not found. Please install it before using the imaging tools. (brew install ffmpeg or apt-get install ffmpeg)")


def get_still_from_video_url(video_url, timestamp, output="/var/tmp/frameshot.png"):
    """
    Takes a video url, a timestamp, and an optional output path/name.
    Downloads the video from the url, takes an image still from given timestamp, and
    saves it as given output.
    """
    assert isinstance(timestamp, (int, float)
                      ), 'invalid option for timestmap, must be int or float.'
    fn = "/var/tmp/tmp_vid.mp4"
    # check if vid exists locally
    if not os.path.isfile(fn):
        rsp = urllib2.urlopen(video_url)
        with open(fn, 'wb') as f:
            f.write(rsp.read())
    # if output exists already delete it as ffmpeg will prompt and hang if it does exist
    if os.path.isfile(output):
        os.remove(output)
    # use ffmpeg to get still from video at timestamp
    subprocess.check_output([ffmpeg, "-ss", str(timestamp), "-i", fn, "-vframes", "1", "-s", "512x288", "-f", "image2", output])
    # if no output assume something went wrong
    if not os.path.isfile(output):
        raise ValueError(
            "Tried to get still image but output doesn't exist after running ffmpeg, please check server logs.")
    # remove video source
    os.remove(fn)
    return output


def get_still_from_video_file(path, timestamp, output="/var/tmp/frameshot.png"):
    """
    Takes a path for a locally stored video, takes a screenshot from the given timestamp and
    saves it as the output path/file.
    """
    assert isinstance(timestamp, (int, float)
                      ), 'invalid option for timestamp, must be int or float.'
    if not os.path.isfile(path):
        raise ValueError("No file found at {}".format(path))
    # if output exists already delete it as ffmpeg will prompt and hang if it does exist
    if os.path.isfile(output):
        os.remove(output)
    # use ffmpeg to get still from video at timestamp
    subprocess.check_output([ffmpeg, "-ss", str(timestamp), "-i", path, "-vframes", "1", "-s", "512x288", "-f", "image2", output])
    # if no output assume something went wrong
    if not os.path.isfile(output):
        raise ValueError(
            "Tried to get still image but output doesn't exist after running ffmpeg, please check server logs.")
    # remove video source
    os.remove(path)
    return output
