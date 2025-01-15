# Image Processing Scripts

This repository contains scripts for processing image files, including updating metadata and converting images to optimized formats for web use.

#### Requirements

- Python 3.7 or higher
- Required libraries:
  - `Pillow`
  - `piexif`

Install the dependencies using pip:

```bash
pip install pillow piexif
```

## Scripts

### 1. Update Image Metadata Script

This script processes image files in a specified directory and updates their metadata with a timestamp extracted from their filenames. It works with JPEG and PNG files and includes error handling and a summary log.

#### Features

- **Metadata Update**: Extracts dates from filenames and updates the `DateTime` metadata for JPEG and PNG images.
- **File Type Analysis**: Counts and logs the number of JPEG, PNG, and video files.
- **Error Handling**: Skips files without valid date patterns or unsupported formats and logs errors.
- **File Type Analysis**: Logs the number of each file type processed (e.g., JPEG, PNG).
- **Summary Log**: Prints a summary of processed, skipped, and failed files.



#### Usage

- Place your image files in a directory (e.g., `samples/`).
- Set the `directory_path` variable in the script to the path of your directory.
- Run the script:

```bash
python update_image_metadata.py
```

---

### 2. Convert Images to WebP Script

This script converts images in a specified directory to the WebP format, optimizing them for web use. It supports common image formats like JPEG, PNG, BMP, and TIFF, and includes options for lossy compression.

#### Features

- **Format Conversion**: Converts images to WebP format for better web performance.
- **Lossy Compression**: Uses adjustable quality settings to balance file size and image quality.
- **File Type Analysis**: Logs the number of each file type processed (e.g., JPEG, PNG).
- **Real-Time Processing**: Prints the name of each file being processed.
- **Summary Log**: Provides a summary of total files scanned, processed, skipped, and any errors encountered.


#### Usage

- Define the input and output directories within the script:
  ```python
  input_directory = "./input_images"
  output_directory = "./output_images"
  ```
- Run the script:

```bash
python convert_images_to_webp.py
```

#### Notes

- The script uses lossy compression with a default quality setting of 75. Adjust this value to reduce file size further or improve image quality.
- Images are resized to a default maximum resolution of 1920x1080 to optimize for web use. You can modify this in the script by changing the max_width and max_height variables.

