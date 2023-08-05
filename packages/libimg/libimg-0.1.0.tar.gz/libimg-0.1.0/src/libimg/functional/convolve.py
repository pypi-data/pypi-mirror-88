from operator import matmul
import numpy as np
import scipy.signal, scipy.stats

import libimg.image
import libimg.math.ops as ops
from libimg.image import Image

def rotate_filter(filter: np.ndarray):
	return filter[::-1,::-1]

class CorrelationalFilter:
	def __init__(self, filt, mode='full', boundary='fill', fillvalue=0):
		assert isinstance(filt, np.ndarray)
		self.filter = filt
		self.mode = mode
		self.boundary = boundary
		self.fillvalue = fillvalue

	def apply(self, image):
		data = np.array(image.data, copy=True)
		for channel in range(image.channels):
			temp = data[:,:,channel]
			data[:,:,channel] = scipy.signal.convolve2d(temp, self.filter, mode=self.mode, boundary=self.boundary, fillvalue=self.fillvalue)
		return Image(data, colorspace=image.colorspace)	

class CustomCorrelationalFilter:
	def __init__(self, filt, force_inseperable=False):
		assert isinstance(filt, np.ndarray)
		self.force_inseperable = force_inseperable
		self.filter = filt

	def apply(self,image):
		if self.force_inseperable or np.linalg.matrix_rank(self.filter) != 1:
			return self._apply_inseperable(image)
		else:
			#
			U, S, V = np.linalg.svd(self.filter, full_matrices=True)
			# This MATLAB blog describes how to use the seperable value function to decompose matricies.
			# https://blogs.mathworks.com/steve/2006/11/28/separable-convolution-part-2/
			# However, MATLAB stores rows/columns in a different order than numpy, so the code is not a direct translation.
			v = np.reshape(U[:,0] * (S[0] ** .5),(S.shape[0], -1))
			h = np.reshape(V[0,:] * (S[0] ** .5), (1,-1))
			return self._apply_seperable(image, v, h)

	def _apply_seperable(self, image, filter1, filter2):
		# Compute size of pad from filter
		xpad, ypad = self.filter.shape
		xpad, ypad = (xpad - 1) // 2, (ypad - 1) // 2
		xsize, ysize, channels = image.dim[0]+2*xpad, image.dim[1]+2*ypad, image.channels
		temp = np.zeros((xsize, ysize, channels))
		data = np.zeros((xsize, ysize, channels))

		# Inset image into middle.
		data[xpad:-xpad,ypad:-ypad,:] = image.data

		# Mirror top/bottom.
		data[0:xpad, ypad:ypad+image.dim[1]] = data[2*xpad:xpad:-1, ypad:ypad+image.dim[1]]
		data[-1:-xpad-1:-1, ypad:ypad+image.dim[1]] = data[-2*xpad:-xpad, ypad:ypad+image.dim[1]]
		for channel in range(image.channels):
			for x in range(xpad, xpad+image.dim[0]):
				for y in range(ypad, ypad+image.dim[1]):
					area = data[x-xpad, y-ypad:y+ypad+1, channel]
					temp[x-xpad,y-ypad,channel] = np.sum(area @ filter1)
		print("Finished top/bottom convolution.")

		# Mirror left/right.
		temp[:, 0:ypad,] = temp[:, 2*ypad:ypad:-1,]
		temp[:, -1:-ypad-1:-1,] = temp[:, -2*ypad:-ypad]

		for channel in range(image.channels):
			for x in range(xpad, xpad+image.dim[0]):
				for y in range(ypad, ypad+image.dim[1]):
					area = temp[x-xpad:x+xpad+1, y-ypad, channel]
					data[x-xpad,y-ypad,channel] = np.sum(filter2 @ area)
		return Image(data[xpad:-xpad:,ypad:-ypad], colorspace=image.colorspace)	

	def _apply_inseperable(self, image):
		# Compute size of pad from filter
		xpad, ypad = self.filter.shape
		xpad, ypad = (xpad - 1) // 2, (ypad - 1) // 2
		xsize, ysize, channels = image.dim[0]+2*xpad, image.dim[1]+2*ypad, image.channels
		output = np.zeros((*image.dim, image.channels))
		data = np.zeros((xsize, ysize, channels))

		# Inset image into middle.
		data[xpad:-xpad,ypad:-ypad,:] = image.data

		# Mirror top/bottom.
		data[0:xpad, ypad:ypad+image.dim[1]] = data[2*xpad:xpad:-1, ypad:ypad+image.dim[1]]
		data[-1:-xpad-1:-1, ypad:ypad+image.dim[1]] = data[-2*xpad:-xpad, ypad:ypad+image.dim[1]]

		# Mirror left/right.
		data[:, 0:ypad,] = data[:, 2*ypad:ypad:-1,]
		data[:, -1:-ypad-1:-1,] = data[:, -2*ypad:-ypad]
	
		for channel in range(image.channels):
			for x in range(xpad, xpad+image.dim[0]):
				for y in range(ypad, ypad+image.dim[1]):
					area = data[x-xpad:x+xpad+1, y-ypad:y+ypad+1, channel]
					output[x-xpad,y-ypad,channel] = np.sum(area * self.filter)
		return Image(output, colorspace=image.colorspace)	

class CustomBoxFilter(CustomCorrelationalFilter):
	def __init__(self, size, force_inseperable=True):
		super(CustomBoxFilter, self).__init__(np.full([2*size+1,2*size+1], fill_value=1.0, dtype=np.float32),
		force_inseperable=force_inseperable)
		self.size = size

	def apply(self, image):
		assert isinstance(image, libimg.image.Image)
		assert image.colorspace == libimg.image.ColorSpace.RGB

		# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
		added = super(CustomBoxFilter, self).apply(image)
		#return added
		return ops.multiply_constant(added, 1.0/(2*self.size+1)**2)

class BoxFilter(CorrelationalFilter):
	def __init__(self, size):
		super(BoxFilter, self).__init__(np.full([2*size+1,2*size+1], fill_value=1.0, dtype=np.float32), mode='same')
		self.size = size

	def apply(self, image):
		assert isinstance(image, libimg.image.Image)
		assert image.colorspace == libimg.image.ColorSpace.RGB

		# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
		added = super(BoxFilter, self).apply(image)
		#return added
		return ops.multiply_constant(added, 1.0/(2*self.size+1)**2)

class GaussianFilter(CorrelationalFilter):
	def __init__(self, size, sigma):
		# Clever approach for generating gaussian filter from:
		#    https://stackoverflow.com/questions/29731726/how-to-calculate-a-gaussian-kernel-matrix-efficiently-in-numpy
		x = np.linspace(-sigma, sigma, 2*size+1)
		# Using the CDF, we can compute a gaussian dist.
		kern1d = np.diff(scipy.stats.norm.cdf(x))
		# Matrix multiply 1d kernel by self to get 2d kernel.
		kern2d = np.outer(kern1d, kern1d)
		self.scale = np.sum(kern2d)
		super(GaussianFilter, self).__init__(kern2d, mode='same')
		self.size = size

	def apply(self, image):
		assert isinstance(image, libimg.image.Image)
		assert image.colorspace == libimg.image.ColorSpace.RGB

		# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
		added = super(GaussianFilter, self).apply(image)
		# We want our number to be in [min, max], so we divide by the sum of all elements
		return ops.multiply_constant(added, 1.0/self.scale)

class InvertFilter(CorrelationalFilter):
	def __init__(self, intensity_range=255):
		super(InvertFilter, self).__init__(np.full([1,1], fill_value=-1.0, dtype=np.float32), mode='same')
		self.intensity_range = intensity_range

	def apply(self, image):
		assert isinstance(image, libimg.image.Image)
		assert image.colorspace == libimg.image.ColorSpace.RGB

		# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
		negated = super(InvertFilter, self).apply(image)
		constant = Image.constantImage(image.channels*(self.intensity_range,), image.dim, colorspace=image.colorspace, as_type=np.float32)

		return ops.add_images(constant, negated)

class LaplacianFilter(CorrelationalFilter):
	def __init__(self, midIsEight=False):
		# Kernel from :
		#    https://homepages.inf.ed.ac.uk/rbf/HIPR2/log.htm
		arr = None
		if midIsEight:
			arr=np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]], dtype=np.float)
		else:
			arr=np.array([[0,-1,0],[-1,4,-1],[0,-1,0]], dtype=np.float)
		super(LaplacianFilter, self).__init__(arr, mode='same', boundary="wrap")

	def apply(self, image):
		assert isinstance(image, libimg.image.Image)
		assert image.colorspace == libimg.image.ColorSpace.RGB

		# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
		result = super(LaplacianFilter, self).apply(image)

		return result

class LaplacianBoost:
	def __init__(self, midIsEight=False):
		super(LaplacianBoost, self).__init__()
		self.laplace = LaplacianFilter(midIsEight=midIsEight)

	def apply(self, image):
		assert isinstance(image, libimg.image.Image)
		assert image.colorspace == libimg.image.ColorSpace.RGB

		# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
		edges = self.laplace.apply(image)
		result = ops.sub_images(image, edges)

		return result

# Unsharp mask:
#    https://theailearner.com/2019/05/14/unsharp-masking-and-highboost-filtering/
class UnsharpFilter:
	def __init__(self, k, radius):
		super(UnsharpFilter, self).__init__()
		self.blur = BoxFilter(radius)
		self.k = k

	def apply(self, image):
		assert isinstance(image, libimg.image.Image)
		assert image.colorspace == libimg.image.ColorSpace.RGB

		# Assume that the caller has taken reasonable steps to ensure that arithmetic overflow will not occur.
		blurred = self.blur.apply(image)
		minuend = ops.multiply_constant(image, self.k + 1)
		subtrahend = ops.multiply_constant(blurred, self.k)
		difference = ops.sub_images(minuend, subtrahend)

		return difference