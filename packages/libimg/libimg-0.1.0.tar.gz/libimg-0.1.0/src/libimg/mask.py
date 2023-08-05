import numpy as np
import more_itertools

import libimg.image

# ABC for vector masks. WIP.
class MaskGeometry():
	pass

# Implement a layer mask (rasterized) in the shape of a rectangle.
class RectangleMask(MaskGeometry):
	def __init__ (self, upper_left, lower_right, value):
		self.upper_left = upper_left
		self.lower_right = lower_right
		self.value = value
		self.mask = np.full((), value)

# A mask collects several mask geoemtries and converts it to a matrix we can perform math on
class Mask:
	def __init__(self, shape, masks):
		masks = more_itertools.always_iterable(masks)
		print(masks)
		self.mask = np.zeros(shape)
		for mask in masks:
			start_x, start_y = mask.upper_left
			end_x, end_y = mask.lower_right
			self.mask[start_y:end_y, start_x:end_x] = mask.mask

	def apply_mask(self, image):
		data = np.array(image.data, copy=True) 
		print(data.shape)
		for channel in range(data.shape[-1]):
			data[:,:,channel] = np.multiply(data[:,:,channel], self.mask)
		return libimg.image.Image(data, image.colorspace)
