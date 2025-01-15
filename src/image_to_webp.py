import os
from pathlib import Path
from PIL import Image


def convert_images_to_webp(input_dir, output_dir):
    """
    Convert images in the specified input directory to WebP format and save them in the output directory.

    :param input_dir: Path to the directory containing images to be converted.
    :param output_dir: Path to the directory where converted images will be saved.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Supported image formats
    supported_formats = {"jpg", "jpeg", "png", "bmp", "tiff", "gif"}

    # Initialize counters for summary
    total_files = 0
    processed_files = 0
    skipped_files = 0
    errors = 0
    file_type_counts = {}  # Dictionary to count processed file types

    # Iterate over all files in the input directory
    for file_path in Path(input_dir).iterdir():
        total_files += 1  # Increment total files counter

        # Check if the file extension is supported
        file_extension = file_path.suffix.lower().lstrip(".")
        if file_extension not in supported_formats:
            skipped_files += 1  # Increment skipped files counter
            continue

        try:
            print(f"Processing file: {file_path.name}")  # Real-time processing message

            # Open the image
            with Image.open(file_path) as img:
                # Set output file path with .webp extension
                output_file = Path(output_dir) / f"{file_path.stem}.webp"

                # Convert to WebP and save with lossles compression
                # img.save(output_file, format="WEBP", lossless=True)  # Lossless conversion (higher quality, larger size)

                # Resize the image to a maximum width and height
                max_width, max_height = 1920, 1080
                img.thumbnail((max_width, max_height))

                # Lossy conversion (optimized for web, smaller size) Modify the quality parameter to adjust the compression level
                img.save(output_file, format="WEBP", quality=75, optimize=True)

                processed_files += 1  # Increment processed files counter

                # Update file type counts
                file_type_counts[file_extension] = (
                    file_type_counts.get(file_extension, 0) + 1
                )
        except Exception as e:
            errors += 1  # Increment errors counter

    # Print summary of the conversion process
    summary = (
        f"\nConversion Summary:\n"
        f"Total files scanned: {total_files}\n"
        f"Files successfully converted: {processed_files}\n"
        f"Files skipped: {skipped_files}\n"
        f"Errors encountered: {errors}\n"
        f"File types processed: "
    )

    # Append file type counts to the summary
    file_type_summary = ", ".join(
        f"{count}{file_type}" for file_type, count in file_type_counts.items()
    )
    summary += file_type_summary

    print(summary)  # Print the final summary


if __name__ == "__main__":
    # Define input and output directories
    input_directory = "./samples"  # Path to the input directory
    output_directory = "./output_images"  # Path to the output directory

    # Call the conversion function with the defined directories
    convert_images_to_webp(input_directory, output_directory)
