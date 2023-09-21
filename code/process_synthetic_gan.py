import cv2
import numpy as np
import os
from PIL import Image

# Define the input and output folders
input_folder = '/Users/jacobcurtis/Desktop/cyclegan_drones/real'
output_folder = '/Users/jacobcurtis/Desktop/cyclegan_drones/fake'
processed_folder = '/Users/jacobcurtis/Desktop/cyclegan_drones/processed'

# count = 0

# Define the size of the output image
output_size = (256, 256)

def crop_transparent_img(img):
    # Load the transparent image
    transparent_img = img.convert('RGBA')

    # Calculate the bounding box around the opaque regions of the transparent image
    bbox = transparent_img.getbbox()

    # Crop the transparent image to the size of the bounding box
    cropped_img = transparent_img.crop(bbox)

    return cropped_img

# Loop over the files in the input folder
for filename in os.listdir(input_folder):
    # Check if the file is a transparent PNG image file
    if filename.endswith('.png') and cv2.imread(os.path.join(input_folder, filename), cv2.IMREAD_UNCHANGED).shape[2] == 4:
        print(filename)
        # Load the image with alpha channel
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # Apply functions
        img = crop_transparent_img(img)
        img_color = np.array(img)[:, :, :3]
        img_alpha = np.array(img)[:, :, 3]

        # Determine the aspect ratio of the cropped image
        aspect_ratio = img_color.shape[1] / img_color.shape[0]

        # Determine the maximum width and height of the scaled image while maintaining the aspect ratio
        if aspect_ratio > 1:
            max_width = output_size[0] - 60  # account for the 30 pixel border on each side
            max_height = int(max_width / aspect_ratio)
        else:
            max_height = output_size[1] - 60  # account for the 30 pixel border on each side
            max_width = int(max_height * aspect_ratio)

        # Scale the image to fit within the output size while maintaining the aspect ratio
        scaled_img = cv2.resize(img_color, (max_width, max_height), interpolation=cv2.INTER_LANCZOS4)

        # Create a black background image with the output size plus the 30 pixel border
        background = np.zeros((output_size[1], output_size[0], 3), dtype=np.uint8)

        # Determine the position to paste the scaled image on the black background, accounting for the 30 pixel border
        y_offset = (output_size[1] - max_height) // 2 + 15
        x_offset = (output_size[0] - max_width) // 2 + 15

        # Paste the scaled image on the black background
        background[y_offset:y_offset+max_height, x_offset:x_offset+max_width] = scaled_img

        # Save the resulting image to the output folder
        cv2.imwrite(os.path.join(processed_folder, filename), background)

        # count += 1
        # if count == 20:
        #     break
