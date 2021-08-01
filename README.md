# white_backgroundify

This script takes input images and pastes them onto a new image with a white background. The new image's width will be `2160`px and its height will be dependent on the mode selected.

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

# Future Considerations

* Make width configurable
* Make output image quality configurable
* Make margin configurable
