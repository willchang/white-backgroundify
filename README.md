# white_backgroundify

---

🚧 **This is a WIP!** 🚧

---

This script takes input images and pastes them onto a new image with a white background. The new image's width will be `2160`px by default (configurable in the script) and its height will be dependent on the mode selected.

Example (images have been scaled down for demonstration purposes):

#### Input Image
![Input image](Images/shadows.jpg)

#### Output Image (using `square` mode)
![Output image](Images/white_bg/shadows_white_bg.jpg)

# Usage

Given a folder `some/folder/with/images` with the following contents:
```
my_image_1.jpg
my_image_2.jpg
my_image_3.jpg
```
Use `white_backgroundify.py` like this:
```
➜ ./white_backgroundify.py --mode=4x5 some/folder/with/images/*.jpg
Created some/folder/with/images/white_bg/my_image_1_white_bg.jpg
Created some/folder/with/images/white_bg/my_image_2_white_bg.jpg
Created some/folder/with/images/white_bg/my_image_3_white_bg.jpg

```

# Modes

Supported modes:
* `square`: The output image will be square.
* `4x5`: The output image will be 4x5.
* `9x16`: The output image will be 9x16.

# Notes

* The output path of each image will be
  ```
  <input image's folder>/white_bg/<input image name>_white_bg.<input image extension>
  ```
  so it's more convenient to use on a single folder with a wildcard path (e.g. `*.jpg`) instead of individual images with separate paths. This is still possible, but you may end up with multiple  `white_bg/` folders if the provided images aren't in the same folder.
* This has only been tested with JPGs. 
* This hasn't been tested much.

# Requirements

* Python 3.7.5
* [Pillow 8.3.1](https://pypi.org/project/Pillow/8.3.1/)

# Why Should You Use This?

Use this if you don't want to faff around with a photo editor's automate/batch function.

# Future Considerations

* Make more options configurable through command line arguments:
  * Width
  * Image quality
  * Margin
* Support more crop formats and modes
* Make modes adaptable (e.g. make 4x5 work with 5x4) – ideal for print
