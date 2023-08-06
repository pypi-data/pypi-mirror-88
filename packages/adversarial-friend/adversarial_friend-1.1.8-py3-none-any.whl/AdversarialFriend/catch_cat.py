import sys
import cv2
import importlib_resources
from os.path import join


def catch_cat():

    image_path = join(
        importlib_resources.files(__package__).as_posix(), 'cat.jpg')

    return image_path
