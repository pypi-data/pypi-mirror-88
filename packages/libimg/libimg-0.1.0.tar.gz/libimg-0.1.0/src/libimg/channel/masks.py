import numpy as np

class NopMask:
    def __init__(self):
        pass
    def apply(self, image):
        return image

class ChannelMask:
    """
    This class allows us to mask out channels of an image.
    """
    def __init__(self, mask):
        self.mask = mask

    def apply(self, image):
        # Images should be rows*columns*components.
        # Require as many components in the mask as components in the image.
        assert(image.shape[2] == len(self.mask))
        return np.multiply(image, self.mask)

class LumincanceBin:
    """
    This class allows us to reduce the number of luminance levels in an image.
    """
    def __init__(self, new_levels, current_levels=256):
        self.new_levels = new_levels
        self.current_levels = current_levels
        bins = [((x)*current_levels/(self.new_levels) + current_levels/(2*self.new_levels))
                for x in range(0, self.new_levels-1)]
        self.levels_bin = np.array(bins)

    def apply(self, image):
        items = np.digitize(image, self.levels_bin, right=False).astype(int)
        items = items * self.current_levels//self.new_levels
        return items