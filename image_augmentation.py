import os
import numpy as np
import logging
from multiprocessing import Pool

import skimage
from skimage.io import imread, imsave
from skimage.transform import rescale, rotate
from skimage.util import random_noise, invert
from skimage.color import rgb2gray
from skimage import exposure

# from image_reader import load_image

import warnings
warnings.filterwarnings("ignore")


def load_image(filename):
    '''
    load image with single thread
    '''
    img_resized = []
    try:
        img = skimage.io.imread(filename)
    except:
        img = skimage.io.imread(filename, plugin='matplotlib')
    return img


class ImageAugmentor():
    '''Class to augment the images

    Attributes:
            in_folder: A string. The path to the directory which contains the images to be
                    augmented, each of the subdirs denotes a class.
            num_thread: An integer. The number of threads to use for augmentation.
            extension: A string. The extension of images to be used in new image's names.
            out_folder: A string. The path to the output directory where new augmented
                    images to be putted. if None, new images will be putted in the in_folder
                    directory.
            verbose: A bool. Whether to show the augmentation info.
    '''

    def __init__(self, in_folder, num_thread=4, extension="jpg", out_folder=None, verbose=True):
        '''Class to augment the images

        Attributes:
                in_folder: A string. The path to the directory which contains the images to be 
                        augmented, each of the subdirs denotes a class.
                num_thread: An integer. The number of threads to use for augmentation. Default
                        is 4.
                extension: A string. The extension of images to be used in new image's names.
                out_folder: A string. The path to the output directory where new augmented 
                        images to be putted. if None, new images will be putted in the in_folder 
                        directory.
        '''
        self.extension = extension
        self.pool = Pool(num_thread)
        self.verbose = verbose
        assert os.path.isdir(in_folder)
        self.in_folder = in_folder
        self.out_folder = out_folder
        if out_folder is not None:
            assert os.path.isdir(out_folder)

    def augmentation(self):
        for subdir in [f for f in os.listdir(self.in_folder) if os.path.isdir(os.path.join(self.in_folder, f))]:
            abs_subdir = os.path.join(self.in_folder, subdir)
            filenames = [os.path.join(abs_subdir, f) for f in os.listdir(
                abs_subdir) if os.path.isfile(os.path.join(abs_subdir, f))]
            if self.out_folder is not None:
                out = "{}/{}".format(self.out_folder, subdir)
                if not os.path.exists(out):
                    os.mkdir(out)
            else:
                out = abs_subdir
            self.pool.map(self.single_augmentation, [
                          (f, out) for f in filenames])

    def single_augmentation(self, args):
        path, out_folder = args
        name = path.split("/")[-1].split(".")[0]
        img = load_image(path)
        self.__augmentation_and_save(self.rescale, name, img, out_folder)
        self.__augmentation_and_save(self.random_noise, name, img, out_folder)
        self.__augmentation_and_save(self.rgb2gray, name, img, out_folder)
        self.__augmentation_and_save(
            self.color_inversion, name, img, out_folder)
        self.__augmentation_and_save(self.rotate_45, name, img, out_folder)
        self.__augmentation_and_save(self.rotate_135, name, img, out_folder)
        self.__augmentation_and_save(self.rotate_225, name, img, out_folder)
        self.__augmentation_and_save(self.rotate_315, name, img, out_folder)
        self.__augmentation_and_save(self.exposure, name, img, out_folder)
        self.__augmentation_and_save(self.gamma, name, img, out_folder)
        self.__augmentation_and_save(
            self.log_correlation, name, img, out_folder)
        self.__augmentation_and_save(
            self.sigmoid_correlation, name, img, out_folder)

    def __augmentation_and_save(self, func, name, img, out_folder):
        new_file_name = '{}/{}'.format(out_folder, name +
                                       "_" + func.__name__ + "." + self.extension)
        imsave(fname=new_file_name, arr=func(img))
        if self.verbose:
            print(func.__name__ + " : " + new_file_name)

    def rescale(self, image):
        return rescale(image, 2.0)

    def random_noise(self, image):
        return random_noise(image)

    def rgb2gray(self, image):
        return rgb2gray(image)

    def color_inversion(self, image):
        return invert(image)

    def rotate_45(self, image):
        return rotate(image, 45)

    def rotate_135(self, image):
        return rotate(image, 135)

    def rotate_225(self, image):
        return rotate(image, 225)

    def rotate_315(self, image):
        return rotate(image, 315)

    def exposure(self, image):
        v_min, v_max = np.percentile(image, (0.2, 99.8))
        return exposure.rescale_intensity(image, in_range=(v_min, v_max))

    def gamma(self, image):
        return exposure.adjust_gamma(image, gamma=0.4, gain=0.9)

    def log_correlation(self, image):
        return exposure.adjust_log(image)

    def sigmoid_correlation(self, image):
        return exposure.adjust_sigmoid(image)

    def __getstate__(self):
        '''
        remove the pool member variable, or get the error when using pool.map(self.load_image)
        '''
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict
