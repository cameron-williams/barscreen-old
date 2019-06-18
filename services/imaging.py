"""
Imaging Tools.
"""
import os
import cv2


def resize_image(image_path, width=512, height=288):
    """
    Takes an image path and resizes it to given dimensions.
    """
    assert os.path.isfile(image_path), "No file found at '{}'".format(image_path)
    image = cv2.imread(image_path)
    image = cv2.resize(image, (width, height))
    cv2.imwrite(image_path, image)
    return True


def screencap_from_video(video_path):
    """
    Takes a video path. Will open that video and captures a frame from
    5 seconds in for a preview image. This image is saved in the same directory
    as the video but as an image instead.
    """
    assert os.path.isfile(video_path), "No file found at '{}'".format(video_path)
    video = cv2.VideoCapture(video_path)

    # Get video filename.
    video_filename = video_path.split("/")[-1].split(".")[0]

    ## Figure out what frame to capture from given video.
    # Get fps of video, as well as total number of frames.
    video_fps = video.get(cv2.CAP_PROP_FPS)
    video_frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)

    # Get the frame number to capture (5 seconds * video frames per second)
    frame_to_capture = round(5 * video_fps)

    # If for some reason the frame to capture is over the total frame count, just set it to 1/4 through the total frame count.
    if frame_to_capture > video_frame_count:
        frame_to_capture = round(video_frame_count / 4)

    # Holds the finished image path.
    video_path = os.path.dirname(video_path)
    image_path = None

    # Read through the video and capture the correct frame.
    current_frame = 0
    while(True):
        ret, frame = video.read()

        if ret:
            # Wait till we are the on the frame that we want to capture.
            if current_frame == frame_to_capture:
                # Resize/write image and break loop.
                image_path = "{}/{}_frame.png".format(video_path, video_filename)
                frame = cv2.resize(frame, (512, 288))
                cv2.imwrite(image_path, frame)
                break

            current_frame += 1
        else:
            break
    
    # Release video and destroy all cv2 windows.
    video.release()
    cv2.destroyAllWindows()

    # Ensure we actually wrote the image.
    if not image_path:
        raise ValueError("unable to get frame from video")
    
    # Return newly created image path.
    return image_path
