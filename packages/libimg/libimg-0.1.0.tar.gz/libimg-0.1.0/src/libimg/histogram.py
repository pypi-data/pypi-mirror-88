import numpy as np
import scipy.signal

import libimg.image
import libimg.math.ops as ops
from libimg.image import Image

def channel_histogram(image, intensity_levels):
	assert isinstance(image, libimg.image.Image)
	assert image.colorspace == libimg.image.ColorSpace.RGB

	histogram = np.ndarray((image.channels))
	for channel in range(image.data.shape[-1]):
		histogram[channel] = np.histogram(image.data[:,:,channel], bins=intensity_levels)

	return histogram

def intensity_histogram(image, intensity_levels):
	assert isinstance(image, libimg.image.Image)
	assert image.colorspace == libimg.image.ColorSpace.RGB
	
	return np.histogram(image.data, bins=intensity_levels)