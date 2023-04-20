import random
import sys

import numpy as np
from PIL import Image


def arnold_cat_map(image, key=(1, 2, 1)):
    """
    Implements Arnold's cat map transformation on an image.
    """
    height, width, *_ = image.shape
    offset_x, offset_y, iterations = key

    new_image = np.zeros(image.shape, dtype=np.uint8)
    for i in range(iterations):
        for x in range(height):
            for y in range(width):
                _x, _y = x, y
                _y = (_y + offset_x * _x) % width
                _x = (_x + offset_y * _y) % height
                new_image[_x, _y] = image[x, y]
    return new_image

def arnold_cat_map_rev(image, key=(1, 2, 1)):
    """
    Implements Arnold's cat map transformation on an image (reverse).
    """
    height, width, *_ = image.shape
    offset_x, offset_y, iterations = key

    new_image = np.zeros(image.shape, dtype=np.uint8)
    for i in range(iterations):
        for x in range(height):
            for y in range(width):
                _x, _y = x, y
                _x = (_x - offset_y * _y) % height
                _y = (_y - offset_x * _x) % width
                new_image[_x, _y] = image[x, y]
    return new_image


def add_watermark(original_image_path, watermark_text_path, output_image_path):
    """
    Adds a text watermark to an image using the Arnold's cat map transformation.
    """

    # Open the original image
    original_image = np.array(Image.open(original_image_path).convert("RGB"))
    height, width, *_ = original_image.shape

    # Open the watermark image
    watermark_image = np.array(Image.open(watermark_text_path).convert("RGB"))
    watermark_height, watermark_width, *_ = watermark_image.shape
    watermark_top = (height - watermark_height) // 2
    if watermark_top < 0:
        print("The height of watermark_text is bigger than original_image")
        sys.exit(1)
    watermark_left = (width - watermark_width) // 2
    if watermark_left < 0:
        print("The width of watermark_text is larger than original_image")
        sys.exit(1)

    # Generator private key
    arnold_dx = random.randint(width // 10, width // 10 * 9)
    arnold_dy = random.randint(height // 10, height // 10 * 9)
    arnold_rd = random.randint(min(height, width) // 10, min(height, width) // 10 * 9)
    private_key = (arnold_dx, arnold_dy, arnold_rd)
    print(f'{private_key = }')

    # Apply the Arnold's cat map transformation to the original image
    transformed_image = arnold_cat_map(original_image, private_key)

    # Add the watermark image to the transformed image
    watermark_image[watermark_image > 0] = 1
    transformed_image[watermark_top:watermark_top+watermark_height, watermark_left:watermark_left+watermark_width] ^= 1 - watermark_image

    # Apply the Arnold's cat map transformation to the transformed image
    output_image = arnold_cat_map_rev(transformed_image, private_key)

    # Save the watermarked image
    Image.fromarray(np.uint8(output_image)).save(output_image_path)

# Check if the command-line arguments are valid
if len(sys.argv) != 4:
    print("Usage: encode.py original_image watermark_text output_image")
    sys.exit(1)

original_image_path = sys.argv[1]
watermark_text_path = sys.argv[2]
output_image_path = sys.argv[3]

# Add the watermark to the original image and save the resulting watermarked image
add_watermark(original_image_path, watermark_text_path, output_image_path)
