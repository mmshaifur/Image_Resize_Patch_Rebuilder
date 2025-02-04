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
