import numpy as np
from sklearn import preprocessing

import libimg.image

def intensity_custom_clip(image, new_min=0, new_max=255, lower_cutoff=0, upper_cutoff=255):

    assert isinstance(image, libimg.image.Image)
    # My clipping algorithm only makes sense for RGB images, not HSL or other more exotic colorspaces.
    assert image.colorspace == libimg.image.ColorSpace.RGB

    data = np.array(image.data, copy=True)
    data[data>upper_cutoff] = new_max
    data[data<lower_cutoff] = new_min

    return libimg.image.Image(data, colorspace=image.colorspace)

def intensity_clip(image, new_min=0, new_max=255):

    assert isinstance(image, libimg.image.Image)
    # My clipping algorithm only makes sense for RGB images, not HSL or other more exotic colorspaces.
    assert image.colorspace == libimg.image.ColorSpace.RGB
    data = np.array(image.data, copy=True)
    data = np.clip(data, new_min, new_max)

    return libimg.image.Image(data, colorspace=image.colorspace)

def intensity_scale_custom_def(data, new_min, new_max):
    re_min = data-np.min(data.reshape(-1))
    re_max = (re_min.astype(np.float32)/np.max(re_min.reshape(-1)))
    data = (((new_max-new_min) * re_max)+new_min).astype(data.dtype)
    return data

def intensity_scale_custom(image, new_min=0, new_max=255):

    assert isinstance(image, libimg.image.Image)
    # My clipping algorithm only makes sense for RGB images, not HSL or other more exotic colorspaces.
    assert image.colorspace == libimg.image.ColorSpace.RGB

    data = np.array(image.data, copy=True)
    data=intensity_scale_custom_def(data, new_min, new_max)

    return libimg.image.Image(data, colorspace=image.colorspace)

def intensity_scale(image, new_min=0, new_max=255):

    assert isinstance(image, libimg.image.Image)
    # My clipping algorithm only makes sense for RGB images, not HSL or other more exotic colorspaces.
    assert image.colorspace == libimg.image.ColorSpace.RGB

    data = np.array(image.data, copy=True)
    scale = preprocessing.MinMaxScaler()
    assert len(data.shape) == 3 and "Image must be 3d array"
    for channel in range(data.shape[-1]):
        temp = scale.fit_transform(data[:,:,channel])
        data[:,:,channel] = ((new_max-new_min)*(temp))
    return libimg.image.Image(data, colorspace=image.colorspace)


def backwards_map(input_image, filter, new_canvas_size):
    pixel_mapping = libimg.image.PixelMapping(input_image, new_canvas_size)
    for x in range(pixel_mapping.new_canvas_size[0]):
        for y in range(pixel_mapping.new_canvas_size[1]):
            pixel_mapping.mapping[x][y] = (filter @ np.asarray([x,y,1]))[0:2]
    #print(pixel_mapping.mapping)
    return pixel_mapping

def interpolate_nearest_neighbor(pixel_mapping, x, y):
    source = pixel_mapping.source_image
    newx, newy = round(x), round(y)
    if (newx < 0 or newx >= source.dim[0]) or (newy < 0 or newy >= source.dim[1]):
        return np.zeros((pixel_mapping.source_image.channels))
    else:
        return pixel_mapping.source_image.data[newx, newy]

def interpolate_bi_linear(pixel_mapping, x, y):
    source = pixel_mapping.source_image
    data = source.data
    lox, hix = np.int(np.floor(x)), np.int(np.ceil(x))
    loy, hiy = np.int(np.floor(y)), np.int(np.ceil(y))
    # If we are on the border, default to nearest neighbor
    if ((lox < 0 or lox >= source.dim[0]) or 
        (hix < 0 or hix >= source.dim[0]) or
        (loy < 0 or loy >= source.dim[1]) or
        (hiy < 0 or hiy >= source.dim[1])):
        return interpolate_nearest_neighbor(pixel_mapping, x, y)
    #print(lox,loy, hix,hiy)

    I_lo_x, I_hi_x, I  = None, None, None
    xmlo, xmhi = np.abs(np.abs(x-lox)), np.abs(np.abs(x-hix))
    ymlo, ymhi = np.abs(np.abs(y-loy)), np.abs(np.abs(y-hiy))
    xhimlo, yhimlo = hix-lox, hiy-loy

    # Interpolate intensities for the x endpoints
    if hiy == loy:
        I_lo_x = data[lox, loy]
        I_hi_x = data[hix, loy]
    else:
        I_lo_x = ((ymlo) / (yhimlo) * (data[lox, loy]) + 
                  (ymhi) / (yhimlo) * (data[lox, hiy]))
        I_hi_x = ((ymlo) / (yhimlo) * (data[hix, loy]) + 
                  (ymhi) / (yhimlo) * (data[hix, hiy]))
        # Figure our where we fall along the line connecting the points.
    if hix == lox:
        I = I_lo_x
    else:
        I = ((xmlo) / (xhimlo) * (I_lo_x) + 
             (xmhi) / (xhimlo) * (I_hi_x))
    return I

def interpolate(pixel_mapping, interp_alg=interpolate_nearest_neighbor):
    source = pixel_mapping.source_image
    channels = source.channels
    data = np.zeros((*pixel_mapping.new_canvas_size, channels), dtype=np.float32)
    for x in range(pixel_mapping.new_canvas_size[0]):
        for y in range(pixel_mapping.new_canvas_size[1]):
            newx, newy = pixel_mapping.mapping[x,y]
            data[x][y] = interp_alg(pixel_mapping, newx, newy)


    return libimg.image.Image(data, colorspace = pixel_mapping.source_image.colorspace)