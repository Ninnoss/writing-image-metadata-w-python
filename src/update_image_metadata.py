import os
import re

import piexif
from PIL import Image, PngImagePlugin


def update_image_metadata(directory):
    date_pattern = re.compile(r"(\d{4}-\d{2}-\d{2})")  # regex pattern to match date in filename

    # keep track of file types and counts
    total_files = 0
    processed_files = 0
    skipped_files = 0
    failed_files = 0
    jpg_files = 0
    png_files = 0
    video_files = 0

    video_extensions = (".mp4", ".mov", ".avi", ".mkv")

    for filename in os.listdir(directory):
        total_files += 1
        filepath = os.path.join(directory, filename)

        # count file types
        if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
            jpg_files += 1
        elif filename.lower().endswith(".png"):
            png_files += 1
        elif filename.lower().endswith(video_extensions):
            video_files += 1

        # process files with date in the filename
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            match = date_pattern.search(filename)
            if match:
                date_str = match.group(1)
                formatted_date = f"{date_str} 00:00:00"

                try:
                    img = Image.open(filepath)

                    # process JPEG files
                    if filename.lower().endswith((".jpg", ".jpeg")):
                        exif_data = img.info.get("exif", None)
                        exif_dict = (
                            piexif.load(exif_data)
                            if exif_data
                            else {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
                        )

                        # Check if date already exists and matches
                        existing_date = exif_dict["Exif"].get(piexif.ExifIFD.DateTimeOriginal, None)
                        if existing_date == formatted_date:
                            skipped_files += 1
                            print(f"Skipped {filename}: Metadata already up-to-date")
                            continue

                        # update metadata
                        exif_dict["0th"][piexif.ImageIFD.DateTime] = formatted_date
                        exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = formatted_date
                        exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = formatted_date

                        exif_bytes = piexif.dump(exif_dict)
                        img.save(filepath, "jpeg", exif=exif_bytes)

                    # process PNG files
                    elif filename.lower().endswith(".png"):
                        metadata = PngImagePlugin.PngInfo()

                        # Check if "DateTime" already exists and matches
                        if "DateTime" in img.info and img.info["DateTime"] == formatted_date:
                            skipped_files += 1
                            print(f"Skipped {filename}: Metadata already up-to-date")
                            continue

                        metadata.add_text("DateTime", formatted_date)
                        img.save(filepath, "png", pnginfo=metadata)

                    processed_files += 1
                    print(f"Updated metadata for {filename}")
                except Exception as e:
                    failed_files += 1
                    print(f"Failed to update metadata for {filename}: {e}")
            else:
                failed_files += 1
                print(f"Skipped {filename}: Date not found in filename")

    # Print summary log
    print("\n=== Summary ===\n")
    print(f"Total files: {total_files}")
    print(f"Files successfully processed: {processed_files}")
    print(f"Files skipped (already up-to-date): {skipped_files}")
    print(f"Files failed to process: {failed_files}")
    print(f"JPEG files: {jpg_files}")
    print(f"PNG files: {png_files}")
    print(f"Video files: {video_files}")


# Set directory to use here
directory_path = "./samples"
update_image_metadata(directory_path)
