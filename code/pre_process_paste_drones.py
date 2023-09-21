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
  new_height = random.randint(10, 50)

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

def paste_drone_image(background, overlay):
  # Load the background image
  background = Image.open(background)

  # Load the transparent image
  overlay = Image.open(overlay).convert('RGBA')

  # Get the dimensions of the background and overlay images
  bg_width, bg_height = background.size
  overlay_width, overlay_height = overlay.size

  # Generate random coordinates within the bounds of the background image
  x = random.randint(0, bg_width - overlay_width)
  y = random.randint(0, bg_height - overlay_height)

  # Check that the overlay image does not exceed the boundaries of the background image
  if x + overlay_width > bg_width:
      x = bg_width - overlay_width
  if y + overlay_height > bg_height:
      y = bg_height - overlay_height

  # Paste the overlay image onto the background image at the specified coordinates
  background.paste(overlay, (x, y), overlay)

  # Save the resulting image
  background.save(img_path+'pasted_drone.png')
  plt.imshow(background)

  #WRITE BOUNDING BOX TO TXT FILE
  # Calculate the coordinates of the bounding box around the pasted image in the YOLO format
  x1, y1 = x, y
  x2, y2 = overlay_width, overlay_height

  # Save the YOLO annotation in a text file
  with open(img_path+'pasted_drone.txt', 'w') as f:
      f.write(f'0 {x1} {y1} {x2} {y2}')

  # Draw bounding boxes
  draw_bounding_boxes(x1, y1, x2, y2)


def draw_bounding_boxes(x1, y1, x2, y2):
    text_file_path=img_path+'pasted_drone.txt'
    with open(text_file_path, 'r') as file:
        line = file.readline().strip()
        values = line.split()
        if len(values) == 5:
            object_class, bbox_x, bbox_y, bbox_w, bbox_h = map(int, values)
        else:
            print(f"Error: line '{line}' in file '{text_file_path}' does not contain 5 values")

    # Load the image and draw the bounding box
    image = cv2.imread(img_path+'pasted_drone.png')
    start_point = (x1, y1)
    end_point = (x1 + x2, y1 + y2)
    color = (0, 255, 0) # Green color
    thickness = 1
    image_with_box = cv2.rectangle(image, start_point, end_point, color, thickness)

    # Save the image with the bounding box
    cv2.imwrite(img_path+'bounding_box.png', image_with_box)
    plt.imshow(image_with_box)


img_path='/content/drive/MyDrive/3D_Model/Pasted_Drones/'
img=Image.open(img_path+'transparent_drone_render.png')
img = crop_transparent_img(img)
img = resize_img(img)

background=img_path+'background_image.png'
overlay=img_path+'resized_drone.png'

paste_drone_image(background, overlay)

