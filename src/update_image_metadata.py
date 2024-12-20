import os
import re

import piexif
from PIL import Image, PngImagePlugin


def update_image_metadata(directory):
    # Regex pattern to match date in filenames in either "YYYY-MM-DD" or "DD-MM-YYYY" formats
    date_pattern = re.compile(r"(\d{4}-\d{2}-\d{2})|(\d{2}-\d{2}-\d{4})")

    # Initialize counters for tracking file processing
    total_files = 0
    processed_files = 0
    skipped_files = 0
    failed_files = 0
    jpg_files = 0
    png_files = 0
    video_files = 0

    # Define video file extensions for tracking
    video_extensions = (".mp4", ".mov", ".avi", ".mkv")

    # Iterate through all files in the given directory
    for filename in os.listdir(directory):
        total_files += 1
        filepath = os.path.join(directory, filename)

        # Count file types based on extensions
        if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
            jpg_files += 1
        elif filename.lower().endswith(".png"):
            png_files += 1
        elif filename.lower().endswith(video_extensions):
            video_files += 1

        # Process image files with a date in the filename
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            match = date_pattern.search(filename)  # Search for date pattern in filename
            if match:
                # Extract the date from the first non-empty capturing group
                date_str = match.group(1) or match.group(2)

                # Convert "DD-MM-YYYY" format to "YYYY-MM-DD" for consistency
                if match.group(2):  # If the second group (DD-MM-YYYY) matched
                    day, month, year = date_str.split("-")
                    date_str = f"{year}-{month}-{day}"

                # Add a default time to the date for metadata
                formatted_date = f"{date_str} 00:00:00"

                try:
                    img = Image.open(filepath)  # Open the image file

                    # Process JPEG files
                    if filename.lower().endswith((".jpg", ".jpeg")):
                        exif_data = img.info.get("exif", None)
                        # Load existing EXIF data or create a new dictionary
                        exif_dict = (
                            piexif.load(exif_data)
                            if exif_data
                            else {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
                        )

                        # Check if the metadata already matches the formatted date
                        existing_date = exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal, None)
                        if existing_date == formatted_date:
                            skipped_files += 1
                            print(f"Skipped {filename}: Metadata already up-to-date")
                            continue

                        # Update EXIF metadata with the new date
                        exif_dict["0th"][piexif.ImageIFD.DateTime] = formatted_date
                        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = formatted_date
                        exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = formatted_date

                        # Save the updated image with new metadata
                        exif_bytes = piexif.dump(exif_dict)
                        img.save(filepath, "jpeg", exif=exif_bytes)

                    # Process PNG files
                    elif filename.lower().endswith(".png"):
                        metadata = PngImagePlugin.PngInfo()

                        # Check if the metadata already matches the formatted date
                        if "DateTime" in img.info and img.info["DateTime"] == formatted_date:
                            skipped_files += 1
                            print(f"Skipped {filename}: Metadata already up-to-date")
                            continue

                        # Add or update the DateTime metadata for PNG
                        metadata.add_text("DateTime", formatted_date)
                        img.save(filepath, "png", pnginfo=metadata)

                    # Increment the processed files counter
                    processed_files += 1
                    print(f"Updated metadata for {filename}")
                except Exception as e:
                    # Handle errors during metadata updates
                    failed_files += 1
                    print(f"Failed to update metadata for {filename}: {e}")
            else:
                # Skip files without a recognizable date in the filename
                failed_files += 1
                print(f"Skipped {filename}: Date not found in filename")

    # Print a summary log of the operation
    print("\n=== Summary ===\n")
    print(f"Total files: {total_files}")
    print(f"Files successfully processed: {processed_files}")
    print(f"Files skipped (already up-to-date): {skipped_files}")
    print(f"Files failed to process: {failed_files}")
    print(f"JPEG files: {jpg_files}")
    print(f"PNG files: {png_files}")
    print(f"Video files: {video_files}")


# Set directory path to the folder containing your files
directory_path = "./samples"
update_image_metadata(directory_path)
