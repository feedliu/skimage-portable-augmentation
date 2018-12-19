from image_augmentation import ImageAugmentor

if __name__ == "__main__":
    # if you want to put new images in the in_folder, just ignore out_folder parameter
    #augmentor = ImageAugmentor("./images")
    augmentor = ImageAugmentor("./images",
                               out_folder="./augmentation", num_thread=8, extension="jpg")
    augmentor.augmentation()
