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
    threshold_range = range(20, 100, 5)
    threshold_range2 = range(-30, 20, 5)

    results_list = []
    for th1 in threshold_range:
        for th2 in threshold_range2:
            try:
                digits_tuple = (ssocr.process_gauss(buf, th1, th2), ssocr.process_mean(buf, th1, th2))
                results_list.append(digits_tuple)
            except Exception:
                pass
    return results_list


def build_dict(results_list):
    values_dict = {}
    for digit_tuple in results_list:
        for digit_list in digit_tuple:
            value = ''
            for digit in digit_list:
                value += str(digit)
            try:
                float_value = float(value)
                if float_value in values_dict:
                    # if values_dict[float_value] >= 20:
                    #     return values_dict
                    values_dict[float_value] += 1
                else:
                    values_dict[float_value] = 0
            except:
                pass
    return values_dict
