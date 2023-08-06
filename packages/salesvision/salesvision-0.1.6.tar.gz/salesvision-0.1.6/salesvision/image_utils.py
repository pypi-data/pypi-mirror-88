import imagehash
import io
import numpy as np
from PIL import Image
import requests


def read_image(image_object):
    """
    Read image by path or URL or Array
    Args:
        image_object: image path on local machine or URL link or Array

    Returns:
        Image in Pillow format or None value if invalid input image object
    """
    if type(image_object) is np.ndarray:
        return Image.fromarray(image_object)

    if type(image_object) is str and len(image_object) == 0:
        return None

    if len(image_object) > 7 and \
            ('http://' == image_object[:7] or 'https://' == image_object[:8]):
        response = requests.get(image_object)
        image_bin = io.BytesIO(response.content)
    else:
        image_bin = open(image_object, "rb")

    image = Image.open(image_bin)

    return image


def compute_image_hash(image: Image):
    """
    Compute image hash
    Args:
        image: image in Pillow format

    Returns:
        string with image hash
    """
    return str(imagehash.average_hash(image))
