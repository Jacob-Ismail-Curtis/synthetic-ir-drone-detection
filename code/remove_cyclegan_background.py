from PIL import Image
import os
import cv2
import numpy as np


def smooth_image():
    # Load the original image
    image = cv2.imread('/Users/jacobcurtis/Desktop/Blender_Drones/Blender_Drones/background_removal/25/B_no_background_padding.png', cv2.IMREAD_UNCHANGED)

    # Create a binary mask where the drone is white (255) and the background is black (0)
    mask = np.where(image[:, :, 3] > 0, 255, 0).astype(np.uint8)

    # Invert the mask to create a background mask
    background_mask = cv2.bitwise_not(mask)

    # Apply the Gaussian blur to the original image using the background mask
    blurred_background = cv2.GaussianBlur(image, (21, 21), 0)
    blurred_background = cv2.bitwise_and(blurred_background, blurred_background, mask=background_mask)

    # Combine the original drone image with the blurred background
    result = cv2.bitwise_or(image, blurred_background)

    # Save the result
    cv2.imwrite('/Users/jacobcurtis/Desktop/Blender_Drones/Blender_Drones/background_removal/25/smoothed_outside_drone.png', result)


def remove_background(image_a, image_b, output_path, border_size=0):
    img_a = Image.open(image_a).convert('RGBA')
    img_b = Image.open(image_b).convert('RGBA')
    width, height = img_a.size
    img_result = Image.new('RGBA', (width, height), (0, 0, 0, 0))

    for y in range(height):
        for x in range(width):
            pixel_a = img_a.getpixel((x, y))
            pixel_b = img_b.getpixel((x, y))

            if pixel_a == (0, 0, 0, 255):  # If pixel in image A is black
                # Check if the pixel is close to a non-black pixel in image A
                is_border = False
                for i in range(-border_size, border_size + 1):
                    for j in range(-border_size, border_size + 1):
                        if 0 <= x + i < width and 0 <= y + j < height:
                            if img_a.getpixel((x + i, y + j)) != (0, 0, 0, 255):
                                is_border = True
                                break
                    if is_border:
                        break

                if is_border:
                    img_result.putpixel((x, y), pixel_b)
                else:
                    img_result.putpixel((x, y), (0, 0, 0, 0))
            else:
                img_result.putpixel((x, y), pixel_b)

    img_result.save(output_path)
def process_image_pairs(real_folder, fake_folder, output_folder, border_size=0):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the list of files in the fake folder
    fake_files = os.listdir(fake_folder)

    # Loop through the files in the fake folder
    for fake_file in fake_files:
        # Check if the file is a PNG image
        if fake_file.endswith('_fake.png'):
            # Extract the file name and extension
            file_name, _ = os.path.splitext(fake_file)

            # Construct the corresponding real file path
            real_file = file_name.replace('_fake', '_real') + '.png'
            real_file_path = os.path.join(real_folder, real_file)

            # Check if the corresponding real file exists
            if os.path.isfile(real_file_path):
                # Construct the output file path
                output_file = file_name.replace('_fake', '_processed') + '.png'
                output_file_path = os.path.join(output_folder, output_file)

                # Remove the background from the image pair
                remove_background(
                    real_file_path,
                    os.path.join(fake_folder, fake_file),
                    output_file_path,
                    border_size
                )


# Define the paths to the real and fake image folders and the output folder
real_folder_path = '/Users/jacobcurtis/Desktop/cg_test/real'
fake_folder_path = '/Users/jacobcurtis/Desktop/cg_test/fake'
output_folder = '/Users/jacobcurtis/Desktop/cg_test/processed'
# Process the image pairs
process_image_pairs(real_folder_path, fake_folder_path, output_folder, border_size=0)