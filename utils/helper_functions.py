import base64
from datetime import datetime
import os
from urllib import request as urllib
import numpy as np
from . import ssocr
import cloudinary
import cloudinary.uploader
import cloudinary.api


def save_image_locally(cedula, image_base64):
    img_name = cedula + " > " + datetime.now().strftime("%d%m%Y %H:%M:%S:%f")
    dir_name = f"images/{cedula}"

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    path = f"{dir_name}/{img_name}"
    with open(path, "wb") as fh:
        fh.write(base64.decodebytes(image_base64))

    return path


def save_image_cloud(user, img_base64):
    data = {}
    img_name = datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")
    #Chequear que se suba bien la foto a cloudinary
    cloudinary_response = cloudinary.uploader.upload("data:image/png;base64," + img_base64, public_id=img_name,
                                                     folder=f'Measures/{user.cedula}')
    data['patient'] = user.id
    data['photo'] = cloudinary_response['url']
    return data


def recognize_digits(img_url):
    img = urllib.urlopen(img_url)
    buf = np.asarray(bytearray(img.read()), dtype="uint8")
    return ssocr.process(buf)