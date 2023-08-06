from tensorflow.python.ops.gen_image_ops import resize_bilinear
from tensorflow.python.ops.array_ops import expand_dims

from tensorflow.python.ops.string_ops import decode_base64
from tensorflow.python.ops.image_ops import decode_image

from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input


def preprocess_image_path(img, img_size, num_channels):
    img = load_img(img, target_size=img_size)
    img = img_to_array(img)
    img = expand_dims(img, 0)
    return preprocess_input(img)


def resize_image_batch(img_batch, img_size):
    return resize_bilinear(img_batch,
                           img_size,
                           half_pixel_centers=True)


def is_image_size_matching(img_shape,
                           img_size,
                           num_channels):
    return img_shape == (img_size[0],
                         img_size[1],
                         num_channels)


# def decode_base64_urlsafe(img):
#     return decode_base64(img)


def decode_base64_not_urlsafe(img):
    img = img.replace('+', '-').replace('/', '_')
    return decode_base64(img)


def preprocess_image_base64(img, img_size, num_channels):
    img = decode_base64_not_urlsafe(img)
    img = decode_image(img,
                       channels=num_channels,
                       expand_animations=False)
    if not is_image_size_matching(img.shape,
                                  img_size,
                                  num_channels):
        img = expand_dims(img, 0)
        img = resize_image_batch(img, img_size)
    else:
        img = img_to_array(img)
        img = expand_dims(img, 0)
    return preprocess_input(img)


def preprocess_image_bytes(img, img_size, num_channels):
    img = decode_image(img,
                       channels=num_channels,
                       expand_animations=False)
    if not is_image_size_matching(img.shape,
                                  img_size,
                                  num_channels):
        img = expand_dims(img, 0)
        img = resize_image_batch(img, img_size)
    else:
        img = img_to_array(img)
        img = expand_dims(img, 0)
    return preprocess_input(img)


def preprocess_image_pillow(img, img_size, num_channels):
    img = img_to_array(img)
    img = expand_dims(img, 0)
    if not is_image_size_matching(img.shape,
                                  img_size,
                                  num_channels):
        img = resize_image_batch(img, img_size)
    return preprocess_input(img)


def preprocess_image(img, img_size, num_channels):
    img_type = type(img)
    if img_type == str:
        if img[-4:] in ['.jpg', '.png', 'jpeg']:
            return preprocess_image_path(img, img_size, num_channels)
        else:
            return preprocess_image_base64(img, img_size, num_channels)
    elif img_type == bytes:
        return preprocess_image_bytes(img, img_size, num_channels)
    else:
        return preprocess_image_pillow(img, img_size, num_channels)


# TODO:
# def preprocess_image_batch(image_batch):
    # pass

