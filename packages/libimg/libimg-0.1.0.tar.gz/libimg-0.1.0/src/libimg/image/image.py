import numpy as np
import skimage.io as io

from .colorspace import ColorSpace
__all__ = ["Image", "PixelMapping"]
class Image:
	"""
	This class encapsulates the behavior of an Image.
	It helps mantain sate about what colorspace an image is in, as well
	as providing a standard reporting mechanism  for the dimensionality of the image.
	"""
	def __init__(self, data, colorspace=ColorSpace.RGB):
		assert len(data.shape) == 3
		self.data = data
		self.colorspace = colorspace
		
		self.channels = data.shape[2]
		self.dim = data.shape[0:2]

	# Create an image of a particular shape with the same number of channels as len(initial_value),
	# with each pixel init'ed to initial_value.
	@staticmethod
	def constantImage(initial_value, shape, colorspace=ColorSpace.RGB, as_type=np.uint8):
		array = np.zeros((*shape,len(initial_value)))
		for index in range(len(initial_value)):
			array[:,:,index:index+1].fill(initial_value[index])
		return Image(array.astype(as_type), colorspace=colorspace)

	# Read in a file and ensure it is X*Y*Channels.
	@staticmethod
	def fromFile(path, colorspace=ColorSpace.RGB, as_type=np.float32):
		data = io.imread(path).astype(as_type)
		if len(data.shape) == 2:
			data = data.reshape(*data.shape, -1)
		return Image(data, colorspace=colorspace)

	# Convert the datatype of the underlying data using an intensity transformation function.
	def changeType(self, newType, intensityFunction):
		self.data = intensityFunction(self.data).astype(newType)

	def changeColorspace(self, newColorSpace):
		assert isinstance(newColorSpace, ColorSpace)
		assert 0 and "Must implement dtype"

class PixelMapping:
    def __init__(self, source_image, new_canvas_size):
        self.source_image = source_image
        # At each entry in the mapping, store the (X,Y) from which the pixel should be sourced.
        self.new_canvas_size=new_canvas_size
        self.mapping = np.zeros((*new_canvas_size, 2), dtype=np.float32)
		

