from PIL import Image, ImageFilter
import os
import random
import shutil

# Define input and output directories
source_img_dir = '/Users/jacobcurtis/Desktop/Blender_Drones/Blender_Drones/demo/pasted_images/images'
source_label_dir = '/Users/jacobcurtis/Desktop/Blender_Drones/Blender_Drones/demo/pasted_images/labels'
dest_img_dir = '/Users/jacobcurtis/Desktop/Blender_Drones/Blender_Drones/demo/motion_blur/images'
dest_label_dir = '/Users/jacobcurtis/Desktop/Blender_Drones/Blender_Drones/demo/motion_blur/labels'

# Define the motion blur strength
# Loop through all files in the source image directory
for filename in os.listdir(source_img_dir):
    # Check if the file is an image
    motion_blur_strength = random.uniform(0, 2)
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Open the image
        img_path = os.path.join(source_img_dir, filename)
        img = Image.open(img_path)

        # Open the corresponding label file
        label_filename = os.path.splitext(filename)[0] + '.txt'
        label_path = os.path.join(source_label_dir, label_filename)
        with open(label_path, 'r') as f:
            line = f.readline().strip()
            values = line.split()
            if len(values) == 5:
                object_class, bbox_x_norm, bbox_y_norm, bbox_w_norm, bbox_h_norm = map(float, values)
            else:
                print(f"Error: line '{line}' in file '{label_path}' does not contain 5 values")
                continue

        # Get the image size
        img_width, img_height = img.size

        # Calculate the actual bounding box values
        bbox_x = bbox_x_norm * img_width
        bbox_y = bbox_y_norm * img_height
        bbox_w = bbox_w_norm * img_width + 2
        bbox_h = bbox_h_norm * img_height + 2

        # Calculate the center point of the bounding box
        x1 = int(bbox_x)
        y1 = int(bbox_y)

        # Calculate the coordinates of the rectangular section to crop
        x2 = int(x1 + bbox_w)
        y2 = int(y1 + bbox_h)
        # Crop the rectangular section from the image
        cropped_img = img.crop((x1, y1, x2, y2))

        # Apply motion blur to the cropped section
        blurred_cropped_img = cropped_img.filter(ImageFilter.BoxBlur(motion_blur_strength))

        # Replace the rectangular section with the blurred one
        img.paste(blurred_cropped_img, (x1, y1, x2, y2))

        # Save the blurred image in the destination image directory
        dest_img_path = os.path.join(dest_img_dir, filename)
        img.save(dest_img_path)

        # Copy the label file to the destination label directory
        dest_label_path = os.path.join(dest_label_dir, label_filename)
        shutil.copy2(label_path, dest_label_path)

print('Finished')
