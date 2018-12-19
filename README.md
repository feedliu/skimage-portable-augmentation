# skimage-portable-augmentation

## Introduction

  Skimage-portable-augmentation is a portable and parallel image augmentor, implemented by skimage(scikit-image) library. If you just want to make a augmentation, and give me a directory to get augmented images, this project actually is what you want.

## Examples

**```in_path```** should be the directory which contain all images, and each of subdirs denotes a class;\
**```out_path```** should be the output directory, and the output directory will have the same structure of subdirs with the in_path;\
**```num_thread```** should be the number of threads to process the augmentation;\
**```extension```** should be the extension to be used when generating new images;\
**```verbose```** should be a bool value to control whether to show the aumentation info.\

if you want to put new images in the in_folder, just ignore out_folder parameter
```python
#augmentor = ImageAugmentor("./images")
augmentor = ImageAugmentor("./images", num_thread=8, extension="jpg", out_folder="./augmentation", verbose=True)
augmentor.augmentation()
```


## Augmentation Types
- color inversion
- exposure
- gamma
- log correlation
- random noise
- rescale
- rgb2gray
- rotate
- sigmoid correlation

Each image will get 12 new images. If you want add new type, just open the file image_augmentation.py.
And add a new member function like this:
```python
def new_type(self, image):
    return new_operation(image)
```
Then add one new line at the end of function **```single_augmentation```**:
```python
self.__augmentation_and_save(self.new_type, name, img, out_folder)
```
It's OK.

<center>

|Type               |Augmented Image|
|:---:|:---:|
| original image | <img src="docs/pics_1_6.jpg" width="400" height="350" />           |
|color inversion    |<img src="docs/pics_1_6_color_inversion.jpg" width="400" height="350" /> |
|exposure           |<img src="docs/pics_1_6_exposure.jpg" width="400" height="350" />        |
|gamma              |<img src="docs/pics_1_6_gamma.jpg" width="400" height="350" />      |
|log correlation    |<img src="docs/pics_1_6_log_correlation.jpg" width="400" height="350" /> |
|random noise       |<img src="docs/pics_1_6_random_noise.jpg" width="400" height="350" />     |
|rescale            |<img src="docs/pics_1_6_rescale.jpg" width="400" height="350" />         |
|rgb2gray           |<img src="docs/pics_1_6_rgb2gray.jpg" width="400" height="350" />        |
|rotate             |<img src="docs/pics_1_6_rotate_45.jpg" width="400" height="350" />       |
|sigmoid correlation|<img src="docs/pics_1_6_sigmoid_correlation.jpg" width="400" height="350" />  |

</center>

## Reference
[kaggle notebook](https://www.kaggle.com/tomahim/image-manipulation-augmentation-with-skimage/notebook)

