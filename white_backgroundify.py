#!/usr/local/bin/python3

import sys
import os
import math
from PIL import Image

# TODO: Add adaptive option so non-square formats aren't strict (e.g. 4x5 can be 5x4, etc.)

# Usage
usage_str = f"""
------------------
This script takes input images and pastes them onto a white background.

Usage: --format=<4x5|2x3|1x1|etc.> <space delimited paths>

--format: A crop format in the form "4x5", "2x3", "1x1", etc.
paths: A space delimited list of file paths.
------------------
"""

# Helpers
def margin(width):
    return math.floor(width * 0.042) # Equivalent to a 1/4" border on a 4x6

# Default config. Change these if desired!
OUTPUT_WIDTH = 2160 # Default
OUTPUT_QUALITY = 95
MARGIN = margin(OUTPUT_WIDTH)

# Options
OPTION_HELP = "--help"
OPTION_WIDTH = "--width"

# Options: Format
OPTION_FORMAT = "--format"
format_str = None
format_width, format_height = 0, 0

# Args
args = sys.argv[1:]
paths = []

# Validate args
while len(args) > 0:
    arg = args[0]
    arg_components = arg.split("=")
    option_name = arg_components[0]
    option_value = arg_components[1] if len(arg_components) == 2 else None

    if option_name == OPTION_HELP:
        print(usage_str)
        sys.exit(0)
    elif option_name == OPTION_FORMAT:
        if not option_value:
            print("Please provide a valid format.")
            sys.exit(1)

        format_str = option_value
        format_components = format_str.split('x')

        if not len(format_components) == 2:
            print("Please provide a valid format.")
            sys.exit(1)

        try:
            format_width, format_height = float(format_components[0]), float(format_components[1])
        except Exception as e:
            print("Please provide a valid format.")
            sys.exit(1)
    elif option_name == OPTION_WIDTH:
        try:
            OUTPUT_WIDTH = math.floor(float(arg_components[1]))
            MARGIN = margin(OUTPUT_WIDTH)

            if OUTPUT_WIDTH <= 0:
                print("Please provide a valid width.")
                sys.exit(1)
        except Exception as e:
            print("Please provide a valid width.")
            sys.exit(1)
        
    else:
        paths.append(arg)

    args = args[1:]

# Validate
if not format_str or format_width == 0 or format_height == 0:
    print("Please provide a valid format.")
    sys.exit(1)

if len(paths) == 0:
    print("Please provide a list of paths.")
    sys.exit(1)

# Process images
skipped_paths = []

for path in paths:
    try:
        # Open image and gather required data
        image = Image.open(path)
        width, height = image.size[0], image.size[1]

        # Path info
        path_components = os.path.split(path) # Split into directory + filename
        filename = path_components[1]
        filename_components = filename.split(".") # Split into filename + extension
        image_name, file_extension = filename_components[0], filename_components[1]

        # Create output dir
        dir_name = os.path.dirname(path)
        if dir_name == "":
            dir_name = "."

        output_dir = f'{dir_name}/white_bg/{format_str}'
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        # Create new image with a white background
        OUTPUT_HEIGHT = math.floor(OUTPUT_WIDTH / (format_width / format_height))
        new_image = Image.new("RGB", (OUTPUT_WIDTH, OUTPUT_HEIGHT), (255, 255, 255))

        # Resize original image
        image_ratio = width / height
        new_width = OUTPUT_WIDTH - MARGIN
        new_height = math.floor(new_width / image_ratio)

        if new_height > OUTPUT_HEIGHT:
            new_height = OUTPUT_HEIGHT - MARGIN
            new_width = math.floor(new_height * image_ratio)

        resized_image = image.resize((new_width, new_height)) 

        # Paste resized image onto new image, centered
        box = (math.floor((OUTPUT_WIDTH - new_width) / 2.0), 
            math.floor((OUTPUT_HEIGHT - new_height) / 2.0))
        new_image.paste(resized_image, box)

        # Save
        new_image_path = f'{output_dir}/{image_name}_white_bg.{file_extension}'
        new_image.save(new_image_path, 
            quality=OUTPUT_QUALITY, 
            icc_profile=image.info['icc_profile'],
            exif=image.info['exif'],
            dpi=(300,300),
            optimize=True)

        print(f'Created {new_image_path}')
    except Exception as e:
        skipped_paths.append(path)
        print(f'Skipping {path}: {e}')

if len(skipped_paths) > 0:
    print(f'\nSkipped {len(skipped_paths)} path(s):\n' + '\n'.join(skipped_paths))
