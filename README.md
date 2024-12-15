# Update Image Metadata Script

This script processes image files in a specified directory and updates their metadata with a timestamp extracted from their filenames. It works with JPEG and PNG files and includes error handling and a summary log.

## Features

- **Metadata Update**: Extracts dates from filenames and updates the `DateTime` metadata for JPEG and PNG images.
- **File Type Analysis**: Counts and logs the number of JPEG, PNG, and video files.
- **Error Handling**: Skips files without valid date patterns or unsupported formats and logs errors.
- **Summary Log**: Prints a summary of processed, skipped, and failed files.

## Requirements

- Python 3.7 or higher
- Required libraries:
  - `Pillow`
  - `piexif`

Install the dependencies using pip:

```bash
pip install pillow piexif
```

## Usage

- Place your image files in a directory (e.g., samples/).
- Set the directory_path variable in the script to the path of your directory.
- Run the script:

```base
python update_image_metadata.py
```
