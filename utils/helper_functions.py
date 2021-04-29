from datetime import datetime
import cloudinary
import cloudinary.uploader
import cloudinary.api





def save_image_cloud(user, img_base64):
    data = {}
    img_name = datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")

    cloudinary_response = cloudinary.uploader.upload("data:image/png;base64," + img_base64, public_id=img_name,
                                                         folder=f'Measures/{user.cedula}')
    data['patient'] = user.id
    data['photo'] = cloudinary_response['url']
    return data