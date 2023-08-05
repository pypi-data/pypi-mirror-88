import numpy as np
import scipy.ndimage

import libimg.image
import libimg.math.ops as ops
from libimg.image import Image


def GammaTransform(image, A=1, gamma=2.2):
	assert isinstance(image, libimg.image.Image)
	assert image.colorspace == libimg.image.ColorSpace.RGB

	# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
	data = np.array(image.data, copy=True)
	data =  A*np.power(data, gamma)

	return Image(data, colorspace=image.colorspace)

def custom_kth_item(image, radius, k):
	data = image.data
	xpad, ypad = radius, radius
	padded = np.pad(data, ((radius,radius),(radius,radius), (0,0)), mode="reflect")
	output = np.zeros(data.shape)
	temp = np.zeros((2*radius+1,2*radius+1))
	for channel in range(image.channels):
		for x in range(xpad, xpad+image.dim[0]):
			for y in range(ypad, ypad+image.dim[1]):
				temp = padded[x-xpad:x+xpad+1, y-ypad:y+ypad+1, channel].reshape(-1)
				#print(temp)
				temp.sort()
				output[x-xpad,y-ypad,channel] = temp[k]
	return Image(output)

def kth_item(image, radius, k):
	return Image(scipy.ndimage.percentile_filter(image.data, 100*(k/radius**2), size=radius))