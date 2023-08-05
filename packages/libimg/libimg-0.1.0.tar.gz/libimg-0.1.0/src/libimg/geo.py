import numpy as np

from libimg.image.image import Image
import libimg.interpolate

def new_canvas_size(image, scale_x, scale_y):
    return int(image.dim[0] * scale_x), int(image.dim[1] * scale_y)

# Rotation is in radians
def create_rotation_mat(rotation, recenter=True):
    return np.asarray([
        [np.cos(rotation), -np.sin(rotation), 0],
        [np.sin(rotation),  np.cos(rotation), 0],
        [0, 0, 1]
    ])

def create_shear_mat(shear_x=0, shear_y=0):
    return np.asarray([
        [1, shear_x, 0],
        [shear_y, 1, 0],
        [0, 0, 1]
    ])
def create_translation_mat(tx, ty):
    return np.asarray([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
def create_scale_mat(scale_x, scale_y):
    return np.asarray([
        [1/scale_x, 0, 0],
        [0, 1/scale_y, 0],
        [0, 0, 1]
    ])

def stack_transforms(transforms):
    T = np.eye(3)
    # Matrix multiply & accumulate.
    for x in transforms:
        T = x @ T
    return T