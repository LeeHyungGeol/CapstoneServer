import numpy as np
import os
from os import listdir
from os.path import isfile, join
from PIL import Image

np.random.seed(3)

from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

data_datagen = ImageDataGenerator(rescale=1. / 255)

data_datagen = ImageDataGenerator(rescale=1. / 255,
                                  rotation_range=5,
                                  shear_range=0.1,
                                 # width_shift_range=0.1,
                                  height_shift_range=0.1,
                                  # zoom_range=1.1,
                                  horizontal_flip=True,
                                  vertical_flip=False,
                                  fill_mode='nearest')

filename_in_dir = []
root_img_dir = 'C:/data/validation/Cabinet'  # 복제할 파일이 들어있는 폴더 경로
change_img_dir = 'C:/data/validation/Cabinet'  # 복제후 파일이 들어있을 폴더 경로
save_file_name = 'img'  # 카테고리 이름

for root, dirs, files in os.walk(root_img_dir):
    for fname in files:
        full_fname = os.path.join(root, fname)
        filename_in_dir.append(full_fname)

for file_image in filename_in_dir:
    print(file_image)
    img = load_img(file_image)
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)

    i = 0

    for batch in data_datagen.flow(x, save_to_dir=change_img_dir, save_prefix=save_file_name, save_format='jpg'):
        i += 1
        if i > 8:
            break