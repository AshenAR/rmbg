import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.utils import CustomObjectScope
from metrics import dice_loss, dice_coef, iou

""" Global parameters """
H = 512
W = 512

""" Creating a directory """
def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def runner(impath):
    np.random.seed(42)
    tf.random.set_seed(42)
    basepath = os.path.dirname(__file__)

    with CustomObjectScope({'iou': iou, 'dice_coef': dice_coef, 'dice_loss': dice_loss}):
        model = tf.keras.models.load_model(basepath+"/model.h5")


    # model.summary()


    # for path in tqdm(impath, total=len(impath)):
    path = impath
    total = len(impath)

    image = cv2.imread(path, cv2.IMREAD_COLOR)
    h, w, _ = image.shape
    x = cv2.resize(image, (W, H))
    x = x/255.0
    x = x.astype(np.float32)
    x = np.expand_dims(x, axis=0)

    y = model.predict(x)[0]
    y = cv2.resize(y, (w, h))
    y = np.expand_dims(y, axis=-1)
    y = y > 0.5

    photo_mask = y
    background_mask = np.abs(1-y)


    masked_photo = image * photo_mask
     # background_mask = np.concatenate([background_mask, background_mask, background_mask], axis=-1)
     # # background_mask = background_mask * [0, 0, 255]
    background_mask = background_mask * [0, 0, 0]

    final_photo = masked_photo + background_mask
    print(final_photo.shape)
    cv2.imwrite("/remove_bg.png", final_photo)
    file_name = "remove_bg.png"


    src = cv2.imread(file_name, 1)
    tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(tmp, 0, 250, cv2.THRESH_BINARY)
    b, g, r = cv2.split(src)
    rgba = [b, g, r, alpha]
    dst = cv2.merge(rgba, 4)
    print(dst)
    cv2.imwrite("/static/test.png", dst)
    return "1"