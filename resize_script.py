# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 00:10:15 2025

@author: snowMan
"""
from PIL import Image, ExifTags
import os

def resize_images(input_dir, output_dir, size=(2048, 2048)):
    """
    Resizes all images in the input directory to the specified size and saves them in the output directory.
    Preserves EXIF orientation.
    
    :param input_dir: Path to the directory containing input images.
    :param output_dir: Path to the directory to save resized images.
    :param size: Tuple indicating the target size (width, height).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        try:
            with Image.open(input_path) as img:
                # Auto-orient image based on EXIF data
                try:
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation] == 'Orientation':
                            break
                    exif = img._getexif()
                    if exif is not None:
                        orientation = exif.get(orientation, None)
                        if orientation == 3:
                            img = img.rotate(180, expand=True)
                        elif orientation == 6:
                            img = img.rotate(270, expand=True)
                        elif orientation == 8:
                            img = img.rotate(90, expand=True)
                except (AttributeError, KeyError, IndexError):
                    pass  # No EXIF data

                img = img.convert("RGB")  # Ensure RGB format
                img = img.resize(size, Image.LANCZOS)  # Resize with high-quality filter
                img.save(output_path)
                print(f"Resized and saved: {output_path}")
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

def create_image_patches(input_dir, output_dir, patch_size=(128, 128)):
    """
    Splits images in the input directory into patches of the specified size and saves them in the output directory.
    
    :param input_dir: Path to the directory containing input images.
    :param output_dir: Path to the directory to save image patches.
    :param patch_size: Tuple indicating the patch size (width, height).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        
        try:
            with Image.open(input_path) as img:
                img = img.convert("RGB")  # Ensure RGB format
                width, height = img.size
                
                for row in range(0, height, patch_size[1]):
                    for col in range(0, width, patch_size[0]):
                        box = (col, row, col + patch_size[0], row + patch_size[1])
                        patch = img.crop(box)
                        patch_filename = f"{os.path.splitext(filename)[0]}_patch_{row}_{col}.jpg"
                        patch.save(os.path.join(output_dir, patch_filename))
                print(f"Created patches for: {filename}")
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

def merge_image_patches(patch_dir, output_dir, original_size, patch_size=(128, 128)):
    """
    Merges image patches back into the original image and saves them with the same name.

    :param patch_dir: Path to the directory containing image patches.
    :param output_dir: Path to the directory to save merged images.
    :param original_size: Tuple indicating the original size (width, height) of the image.
    :param patch_size: Tuple indicating the patch size (width, height).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Collect valid patches with expected format
    patch_files = []
    for f in os.listdir(patch_dir):
        parts = f.split('_patch_')
        if len(parts) == 2 and parts[1].count('_') == 1:
            patch_files.append(f)

    # Sort patches based on row and column values
    patch_files = sorted(patch_files, key=lambda x: tuple(map(int, x.split('_patch_')[1].split('.')[0].split('_'))))

    # Create new blank image
    merged_image = Image.new("RGB", original_size)

    # Paste patches in the correct order
    for patch_filename in patch_files:
        patch_path = os.path.join(patch_dir, patch_filename)
        patch = Image.open(patch_path)

        try:
            row, col = map(int, patch_filename.split('_patch_')[1].split('.')[0].split('_'))
            merged_image.paste(patch, (col, row))
        except ValueError:
            print(f"Skipping invalid patch filename: {patch_filename}")

    # Save the merged image using the original filename
    original_filename = patch_files[0].split('_patch_')[0] + "_merged.jpg"
    output_path = os.path.join(output_dir, original_filename)
    merged_image.save(output_path)
    print(f"Merged image saved at: {output_path}")
    
def merge_all_images_with_missing_patches(patch_dir, output_dir, original_size, patch_size=(128, 128)):
    """
    Merges image patches back into their original images, filling missing patches with black and preserving their original names.
    
    :param patch_dir: Path to the directory containing image patches.
    :param output_dir: Path to the directory to save merged images.
    :param original_size: Tuple indicating the original size (width, height) of the images.
    :param patch_size: Tuple indicating the patch size (width, height).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    image_names = set(f.split('_patch_')[0] for f in os.listdir(patch_dir) if '_patch_' in f)
    
    for base_name in image_names:
        merged_image = Image.new("RGB", original_size, (0, 0, 0))
        
        for row in range(0, original_size[1], patch_size[1]):
            for col in range(0, original_size[0], patch_size[0]):
                patch_filename = f"{base_name}_patch_{row}_{col}.jpg"
                patch_path = os.path.join(patch_dir, patch_filename)
                
                if os.path.exists(patch_path):
                    patch = Image.open(patch_path)
                else:
                    patch = Image.new("RGB", patch_size, (0, 0, 0))  # Create black patch for missing areas
                
                merged_image.paste(patch, (col, row))
        
        output_filename = f"{base_name}_merged.jpg"
        output_path = os.path.join(output_dir, output_filename)
        merged_image.save(output_path)
        print(f"Merged image with missing patches filled saved at: {output_path}")

# Example usage
input_directory = r"D:\Git_clone\Large-Image-Patching-and-Marging\input"  # Use raw string (r"...") to avoid escape issues
output_directory = r"D:\Git_clone\Large-Image-Patching-and-Marging\resized"
resize_images(input_directory, output_directory)
patch_output_directory = r"D:\Git_clone\Large-Image-Patching-and-Marging\patches"
create_image_patches(output_directory, patch_output_directory)
merged_output_directory = r"D:\Git_clone\Large-Image-Patching-and-Marging\marged"
merge_all_images_with_missing_patches(patch_output_directory, merged_output_directory, (2048, 2048))