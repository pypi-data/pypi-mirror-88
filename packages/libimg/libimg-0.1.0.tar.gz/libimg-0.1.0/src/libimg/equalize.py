import numpy as np
import scipy.signal

import libimg.image
import libimg.math.ops as ops
from libimg.image import Image
import libimg.interpolate as interp

def stretch_contrast(image, new_min=0, new_max=255,clip_min=None, clip_max=None):
	assert isinstance(image, libimg.image.Image)
	# My clipping algorithm only makes sense for RGB images, not HSL or other more exotic colorspaces.
	assert image.colorspace == libimg.image.ColorSpace.RGB

	data = np.array(image.data, copy=True)
	
	# Clip out the portions we don't care about.
	# We default to the min/max values of the image, but the user can clip more if they want
	clip_min = clip_min if clip_min != None else np.min(data.reshape(-1))
	clip_max = clip_max if clip_max != None else np.max(data.reshape(-1))
	data = np.clip(data, clip_min, clip_max)
	
	# Linearly stretch the clipped image to fill the new range [new_min, new_max] using  lerp.
	data = interp.intensity_scale_custom_def(data, new_min, new_max)

	return Image(data, colorspace=image.colorspace)

def local_hist(data, bins, min_val, max_val):
	channels = data.shape[-1]
	# Compute per-channel histogram.
	hist = np.zeros((channels, bins), dtype=np.int32)
	for channel in range(channels):
		for pixel in data[:,:,channel].flatten():
			pixel = int(pixel)
			if pixel <= min_val:
				hist[channel][0] += 1
			elif pixel >= max_val:
				hist[channel][bins-1] += 1
			else:
				hist[channel][pixel] += 1
	return hist
def cdf_remap_reuse_mem(data, histogram, cdf, new_val, bins, min_val, max_val):
	channels = data.shape[-1]
	pixels = data.shape[0]*data.shape[1]
	cdf.fill(0.0)
	new_val.fill(0)
	for channel in range(channels):
		mincdf = histogram[channel][0]
		cdf[channel][0] = histogram[channel][0]
		for index in range(1, bins):
			cdf[channel][index] = histogram[channel][index] + cdf[channel][index-1]
		for index in range(0, bins):
			new_val[channel][index] = ((cdf[channel,index] - mincdf)/ (pixels-mincdf+1)) * (max_val-min_val-2) + 1
			
def cdf_remap(data, histogram, bins, min_val, max_val):
	channels = data.shape[-1]
	cdf = np.zeros((channels, bins), dtype=np.float)
	new_val = np.zeros((channels, bins), dtype=np.uint8)
	cdf_remap_reuse_mem(data, histogram, cdf, new_val, bins, min_val, max_val)
	return cdf, new_val

def global_equalize_histogram(image, intensity_levels=256, min_val=0, max_val=255):
	assert isinstance(image, libimg.image.Image)
	assert image.colorspace == libimg.image.ColorSpace.RGB
	# Compute per-channel histogram.
	hist = local_hist(image.data, intensity_levels, min_val, max_val)
	# Compute CDF
	cdf, new_val = cdf_remap(image.data, hist, intensity_levels, min_val, max_val)
	# print(new_val)
	# Perform pixel substitution.
	data = np.zeros((*image.dim, image.channels))
	for channel in range(image.channels):
		for d1 in range(image.dim[0]):
			for d2 in range(image.dim[1]):
				pixel = int(image.data[d1,d2,channel])
				nval = new_val[channel,pixel]
				data[d1,d2,channel] = nval

	return Image(data, colorspace=image.colorspace)

def local_equalize_histogram(image, neighborhood=1, intensity_levels=256, min_val=0, max_val=255):
	assert isinstance(image, libimg.image.Image)
	assert image.colorspace == libimg.image.ColorSpace.RGB
	data = np.zeros((2*neighborhood+image.dim[0],2*neighborhood+image.dim[1], image.channels))
	result = np.zeros((image.dim[0], image.dim[1], image.channels))
	data[neighborhood:-neighborhood, neighborhood:-neighborhood, :]=image.data

	channels = data.shape[-1]

	cdf = np.zeros((channels, intensity_levels), dtype=np.float)
	new_val = np.zeros((channels, intensity_levels), dtype=np.uint8)

	for channel in range(image.channels):
		for d1 in range(neighborhood, neighborhood+image.dim[0]):
			print(d1)
			for d2 in range(neighborhood, neighborhood+image.dim[1]):
				subregion = data[d1-neighborhood:d1+neighborhood+1, d2-neighborhood:d2+neighborhood+1,:]
				# Compute per-channel histogram.
				hist = local_hist(subregion, intensity_levels, min_val, max_val)
				# Compute CDF
				cdf_remap_reuse_mem(subregion, hist, cdf, new_val, intensity_levels, min_val, max_val)
				pixel = int(data[d1,d2,channel])
				nval = new_val[channel,pixel]
				result[d1-neighborhood,d2-neighborhood,channel] = nval
	
	return Image(result, colorspace=image.colorspace)