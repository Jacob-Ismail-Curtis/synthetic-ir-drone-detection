from PIL import Image
import matplotlib.pyplot as plt
import random, cv2, os
import numpy as np

def crop_transparent_img(img):

  # Load the transparent image
  transparent_img = img.convert('RGBA')

  # Get the dimensions of the transparent image
  transparent_width, transparent_height =   transparent_img = img.convert('RGBA').size

  # Calculate the coordinates of the bounding box around the opaque regions of the transparent image
  bbox =  transparent_img = img.convert('RGBA').getbbox()

  # Crop the transparent image to the size of the bounding box
  cropped_img =  transparent_img = img.convert('RGBA').crop(bbox)

  # Save the resulting image
  cropped_img.save(img_path+'cropped_drone.png')

  return cropped_img


def resize_img(img):
  # Get the original width and height
  orig_width, orig_height = img.size

  # Randomly generate a new height
  new_height = random.randint(10, 40)

  # Calculate the scaling factor
  scaling_factor = new_height / orig_height

  # Calculate the new width
  new_width = int(orig_width * scaling_factor)

  # Resize the image while maintaining aspect ratio
  resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)
  # Save the resized image
  plt.imshow(resized_img)
  resized_img.save(img_path+'resized_drone.png')

  return resized_img

# Define the paths of input and output directories
input_dir = '/Users/jacobcurtis/Desktop/Blender_Drones/Blender_Drones/blurred_images'
output_dir = '/Users/jacobcurtis/Desktop/Blender_Drones/Blender_Drones/pre_processed_images'

# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    # Check if the file is an image
    if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
        # Open the image
        img_path = os.path.join(input_dir, filename)
        img = Image.open(img_path)

        # Apply functions
        img=crop_transparent_img(img)
        img=resize_img(img)


        # Save the new image with the same name in the output directory
        output_path = os.path.join(output_dir, filename)
        img.save(output_path)

print('Finished')


# background=img_path+'background_image.png'
# overlay=img_path+'resized_drone.png'

# paste_drone_image(background, overlay)
