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


def extract_watermark(original_image_path, watermarked_image_path, output_image_path, private_key):
    """
    Extracts a text watermark from a watermarked image using the Arnold's cat map transformation.
    """

    # Open the original image
    original_image = np.array(Image.open(original_image_path).convert("RGB"))

    # Open the watermarked image
    watermarked_image = np.array(Image.open(watermarked_image_path).convert("RGB"))
    assert watermarked_image.shape == original_image.shape

    # Extract the watermark from the watermarked image
    original_image ^= watermarked_image
    transformed_image = arnold_cat_map(original_image, private_key)
    transformed_image[transformed_image > 0] = 255
    transformed_image = 255 - transformed_image

    # Save the extracted watermark
    Image.fromarray(np.uint8(transformed_image)).save(output_image_path)

# Check if the command-line arguments are valid
if len(sys.argv) != 7:
    print("Usage: decode.py original_image watermarked_image output_image arnold_dx arnold_dy arnold_rd")
    sys.exit(1)

original_image_path = sys.argv[1]
watermarked_image_path = sys.argv[2]
output_image_path = sys.argv[3]
private_key = tuple(map(int, sys.argv[4:7]))

# Extract the watermark from the watermarked image
extract_watermark(original_image_path, watermarked_image_path, output_image_path, private_key)
