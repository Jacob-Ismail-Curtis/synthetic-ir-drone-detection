import os
from PIL import Image, ImageFilter
import random

# Define the paths of input and output directories
input_dir = '/Users/jacobcurtis/Desktop/Blender_Drones/Blender_Drones/demo/synthetic_images'
blurred_dir = '/Users/jacobcurtis/Desktop/Blender_Drones/Blender_Drones/demo/blurred_images'
# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    # Check if the file is an image
    if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
        # Open the image
        img_path = os.path.join(input_dir, filename)
        img = Image.open(img_path)

        # Apply Gaussian blur with random kernel size between 0 and 1
        gaussian_blur_level = random.uniform(0.3, 2)
        img = img.filter(ImageFilter.GaussianBlur(gaussian_blur_level))

        # Save the new image with the same name in the output directory
        output_path = os.path.join(blurred_dir, filename)
        img.save(output_path)
print('Finished')