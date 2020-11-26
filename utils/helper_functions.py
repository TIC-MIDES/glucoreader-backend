import base64
from datetime import datetime
import os
from urllib import request as urllib
import numpy as np
from . import ssocr
import cloudinary
import cloudinary.uploader
import cloudinary.api
from PIL import Image, ImageEnhance
from io import BytesIO
import cv2
import io
from imageio import imread
import matplotlib.pyplot as plt

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

    image = imread(io.BytesIO(base64.b64decode(img_base64)))

    orig = image.copy()

    template = cv2.imread("./static/glucometro.png", 0)  # real_target_common.png

    # cv2.imshow("Image", template)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    height, width = template.shape[::]

    res = cv2.matchTemplate(img_gray, template, cv2.TM_SQDIFF)
    plt.imshow(res, cmap='gray')

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = min_loc  # Change to max_loc for all except for TM_SQDIFF
    bottom_right = (top_left[0] + width, top_left[1] + height)
    cv2.rectangle(image, top_left, bottom_right, (255, 0, 0), 2)
    # image = image[top_left[1]:top_left[1]+height, top_left[0]:top_left[0]+width]
    # cv2.imshow("Matched image", image)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    # # convert to grayscale
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # edged = cv2.Canny(image, 170, 490)
    # # Apply adaptive threshold
    # thresh = cv2.adaptiveThreshold(edged, 255, 1, 1, 11, 2)

    # # apply some dilation and erosion to join the gaps - change iteration to detect more or less area's
    # thresh = cv2.dilate(thresh, None, iterations=1)
    # thresh = cv2.erode(thresh, None, iterations=1)

    # # Find the contours
    # contours, hierarchy = cv2.findContours(thresh,
    #                                        cv2.RETR_TREE,
    #                                        cv2.CHAIN_APPROX_SIMPLE)
    # # For each contour, find the bounding rectangle and draw it
    # for cnt in contours:
    #     x, y, w, h = cv2.boundingRect(cnt)
    #     cv2.rectangle(image,
    #                   (x, y), (x+w, y+h),
    #                   (0, 255, 0),
    #                   2)


    # cv2.imshow('img', thresh)
    # cv2.imshow('img2', image)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(blurred, 0, 255, 1)
        
    # thresh = cv2.adaptiveThreshold(edges, 255, 1, 1, 11, 2)
    # thresh = cv2.dilate(thresh, None, iterations=1)
    # thresh = cv2.erode(thresh, None, iterations=0)
    # Finding and sorting contours based on contour area
    cnts = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    vertices = []
    max_rectangle = 0
    for i, c in enumerate(cnts):
        peri = cv2.arcLength(cnts[i], True)
        approx = cv2.approxPolyDP(cnts[i], 0.02 * peri, True)
        if len(approx) >= 4:
            x, y, w, h = cv2.boundingRect(approx)
            # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if w/h>1.4 and w/h<1.8 and w*h>max_rectangle: # RECTANGLE RATIO
                # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                max_rectangle = w*h
                rectangle = approx
                if not vertices:
                    vertices.append(rectangle)
                else:
                    vertices[0] = rectangle
    if vertices:
        x, y, w, h = cv2.boundingRect(vertices[0])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    roi = image[y:y+h, x:x+w]

    im = Image.fromarray(np.uint8(roi))
    basesize = 300 # Tamaño 
    percent = 1
    if im.height > basesize and im.height > im.width:
        percent = float((basesize/float(im.height)))
    elif im.width > basesize:
        percent = float(basesize/float(im.width))
    height = int(im.height * percent)
    width = int(im.width * percent)
    im.thumbnail((width, height), Image.ANTIALIAS)
    byte_io = BytesIO()
    im.save(byte_io, 'PNG')
    byte_io.seek(0)


    # imS = cv2.resize(image, (340, 640))                    # Resize image
    # cv2.imshow("Lines", edges)
    # cv2.imshow("Input", roi)
    # cv2.imshow("Contour", imS)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    original = Image.fromarray(np.uint8(orig))

    byte_original = BytesIO()
    original.save(byte_original, 'PNG')
    byte_original.seek(0)
    
    cloudinary_response = cloudinary.uploader.upload(byte_io, public_id=img_name,
                                                     folder=f'Measures/{user.cedula}')
    data['patient'] = user.id
    data['photo'] = cloudinary_response['url']
    return data


def recognize_digits(img_url):
    img = urllib.urlopen(img_url)

    im = Image.open(BytesIO(img.read()))
    enhancer = ImageEnhance.Brightness(im)
    factor = range(1, 6, 1) # change the brightness

    threshold_range = range(20, 80, 10)
    threshold_range2 = range(-40, 20, 10)

    results_list = []
    for brightness in factor:
        im_output = enhancer.enhance(brightness)
        buffered = BytesIO()
        im_output.save(buffered, format="png")
        buf = np.asarray(bytearray(buffered.getvalue()), dtype="uint8")
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
