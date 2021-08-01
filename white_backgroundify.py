#!/usr/local/bin/python3

import sys
import os
import math
from PIL import Image

# Modes
MODE_SQUARE = "square"
MODE_4x5 = "4x5"
modes = [MODE_SQUARE, MODE_4x5]

# Usage
usage_str = f"""
------------------
This script takes input images and pastes them onto a white background.

Usage: --mode=<mode> <space delimited paths>

--mode: One of {modes}. The output file will be this format.
paths: A space delimited list of file paths.
------------------
"""

# Input
command = sys.argv[1]
paths = sys.argv[2:]

# Constants
MARGIN = 40
OUTPUT_WIDTH = 2160
OUTPUT_HEIGHT_SQUARE = OUTPUT_WIDTH
OUTPUT_HEIGHT_4x5 = 2700
OUTPUT_HEIGHT = 0 # Give the output height a default
OUTPUT_QUALITY = 95

# Validate inputs
if command == "--help":
    print(usage_str)
    sys.exit(0)
elif command[:7] == "--mode=":
    mode = command[7:]

    if not mode in modes:
        print(f"Error: Unrecognized mode.\n{usage_str}")
        sys.exit(1)
else:
    raise Exception("Unrecognized command.")

if len(paths) == 0:
    print(f"Error: please provide a list of paths.\n{usage_str}")
    sys.exit(1)

# Configuration
if mode == MODE_SQUARE:
    OUTPUT_HEIGHT = OUTPUT_HEIGHT_SQUARE
elif mode == MODE_4x5:
    OUTPUT_HEIGHT = OUTPUT_HEIGHT_4x5
else:
    raise Exception("There was a problem configuring output height based on mode.")

if OUTPUT_HEIGHT == 0:
    raise Exception("There was a problem configuring output height.")

# Process images
skipped_paths = []

for path in paths:
    try:
        # Open image and gather required data
        im = Image.open(path)
        width = im.size[0]
        height = im.size[1]
        dir_name = os.path.dirname(path)
        path_splitted = os.path.split(path)
        filename = path_splitted[1]
        filename_splitted = filename.split(".")
        image_name = filename_splitted[0]
        file_extension = filename_splitted[1]

        # Create output dir
        if dir_name == "":
            dir_name = "."
            
        white_bg_dir = f'{dir_name}/white_bg'
        if not os.path.isdir(white_bg_dir):
            os.mkdir(white_bg_dir)

        # Create new image with a white background
        new_im = Image.new("RGB", (OUTPUT_WIDTH, OUTPUT_HEIGHT), (255, 255, 255))

        # Resize original image
        image_ratio = width / height
        new_width = 0
        new_height = 0

        if width > height:
            new_width = OUTPUT_WIDTH - MARGIN
            new_height = math.floor(new_width / image_ratio)
        else:
            new_height = OUTPUT_HEIGHT - MARGIN
            new_width = math.floor(new_height * image_ratio)

        resized_im = im.resize((new_width, new_height)) 

        # Paste resized image onto new image, centered
        box = (math.floor((OUTPUT_WIDTH - new_width) / 2.0), 
            math.floor((OUTPUT_HEIGHT - new_height) / 2.0))
        new_im.paste(resized_im, box)

        # Save
        new_path_path = f'{white_bg_dir}/{image_name}_white_bg.{file_extension}'
        new_im.save(new_path_path, 
            quality=OUTPUT_QUALITY, 
            icc_profile=im.info['icc_profile'],
            exif=im.info['exif'])

        print(f'Created {new_path_path}')
    except Exception as e:
        skipped_paths.append(path)
        print(f'Skipping {path}: {e}')

if len(skipped_paths) > 0:
    print(f'\nSkipped {len(skipped_paths)} path(s):\n' + '\n'.join(skipped_paths))
