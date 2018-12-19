import logging
from image_augmentation import ImageAugmentor

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(levelname)s : %(message)s',
                        datefmt='%Y/%m/%d %H:%M:%S',
                        level=logging.DEBUG)
    # if you want to put new images in the in_folder, just ignore out_folder parameter
    #augmentor = ImageAugmentor("/home/feedliu/Documents/skimage-portable-augmentation/images")
    augmentor = ImageAugmentor("./images",
                               out_folder="./augmentation", num_thread=8, extension="jpg")
    augmentor.augmentation()
