# Image Resizing and Patching Utility

## Overview
This project provides a Python utility to:
- **Resize images** to a specified resolution (default: 2048x2048).
- **Create image patches** of a fixed size (default: 128x128).
- **Merge patches back into the original image** while handling missing patches by filling them with black.

## Features
✔ Supports bulk image processing from directories.  
✔ Preserves image EXIF orientation during resizing.  
✔ Handles missing patches while merging images.  
✔ Outputs merged images with the original filename.  

## Installation
### Prerequisites
Ensure you have **Python 3.6+** installed and install the required dependencies:

```bash
pip install pillow
```

## Usage

### 1. Resizing Images
Resize images from an input directory and save them in an output directory:

```python
resize_images(input_dir="path/to/input", output_dir="path/to/output")
```

### 2. Creating Image Patches
Split images into smaller **128x128** patches:

```python
create_image_patches(input_dir="path/to/output", output_dir="path/to/patches")
```

### 3. Merging Patches Back Into an Image
Reconstruct the original images from patches while handling missing patches:

```python
merge_all_images_with_missing_patches(patch_dir="path/to/patches",
                                      output_dir="path/to/merged",
                                      original_size=(2048, 2048))
```

## Folder Structure
```
📂 project-root
 ├── 📂 input/        # Raw images
 ├── 📂 output/       # Resized images
 ├── 📂 patches/      # Image patches
 ├── 📂 merged/       # Reconstructed images
 ├── resize_script.py # Python script
 ├── README.md        # Documentation
```

## License
This project is licensed under the MIT License.

## Contributions
Pull requests and suggestions are welcome!

