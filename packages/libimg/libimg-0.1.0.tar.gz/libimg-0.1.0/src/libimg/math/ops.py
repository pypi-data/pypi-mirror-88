import numpy as np

import libimg.image
from libimg.image import Image

def multiply_constant(image, constant):
	# Require that both inputs are images and in the same colorspace
	assert isinstance(image, libimg.image.Image)
	# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
	out = image.data * constant
	return Image(out, colorspace=image.colorspace)

def multiply_images(upper, lower):
	# Require that both inputs are images and in the same colorspace
	assert isinstance(lower, libimg.image.Image)
	assert isinstance(upper, libimg.image.Image)
	assert upper.colorspace == lower.colorspace
	# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
	out = upper.data * lower.data
	return Image(out, colorspace=upper.colorspace)

def reciprocal(image):
	assert isinstance(image, libimg.image.Image)
	assert image.colorspace == libimg.image.ColorSpace.RGB

	# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
	out = 1 / image.data

	return Image(out, colorspace=image.colorspace)

def add_constant(image, constant):
	# Require that both inputs are images and in the same colorspace
	assert isinstance(image, libimg.image.Image)
	# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
	out = image.data + constant
	return Image(out, colorspace=image.colorspace)

def add_images(upper, lower):
	# Require that both inputs are images and in the same colorspace
	assert isinstance(lower, libimg.image.Image)
	assert isinstance(upper, libimg.image.Image)
	assert upper.colorspace == lower.colorspace

	# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
	out = upper.data + lower.data

	return Image(out, colorspace=upper.colorspace)

def sub_constant(image, constant):
	# Require that both inputs are images and in the same colorspace
	assert isinstance(image, libimg.image.Image)
	# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
	out = image.data - constant
	return Image(out, colorspace=image.colorspace)

def sub_images(upper, lower):
	# Require that both inputs are images and in the same colorspace
	assert isinstance(lower, libimg.image.Image)
	assert isinstance(upper, libimg.image.Image)
	assert upper.colorspace == lower.colorspace

	# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
	out = upper.data - lower.data

	return Image(out, colorspace=upper.colorspace)

def abs_dif(upper, lower):
	
	# Require that both inputs are images and in the same colorspace
	assert isinstance(lower, libimg.image.Image)
	assert isinstance(upper, libimg.image.Image)
	assert upper.colorspace == lower.colorspace

	# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
	first = np.abs(upper.data - lower.data)
	second = np.abs(lower.data - upper.data)

	return Image(np.minimum(first, second), colorspace=upper.colorspace)