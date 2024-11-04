import os
import shutil
import time
import csv

# Function to create a date-based directory structure
def create_date_directory(base_dir):
    today_date = time.strftime("%Y-%m-%d")
    date_dir = os.path.join(base_dir, today_date)

    # Subdirectories for CSV, DAT, and other files within the date folder
    csv_dir = os.path.join(date_dir, 'csv_files')
    dat_dir = os.path.join(date_dir, 'dat_files')
    others_dir = os.path.join(date_dir, 'others')

    for directory in [date_dir, csv_dir, dat_dir, others_dir]:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
        except OSError as e:
            print(f"Error creating directory {directory}: {str(e)}")

    return csv_dir, dat_dir, others_dir

# Function to validate CSV files
def is_valid_csv(file_path):
    try:
        with open(file_path, 'r', newline='') as csvfile:
            # Attempt to read as CSV to check for format validity
            csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)  # Reset read position for any further processing
        return True
    except (csv.Error, UnicodeDecodeError) as e:
        print(f"Invalid CSV format detected for file {file_path}: {str(e)}")
        return False

# Function to move file and handle duplicates using timestamp
def duplicate_file_handler(src_path, dest_dir):
    try:
        filename = os.path.basename(src_path)
        dest_path = os.path.join(dest_dir, filename)

        # Check if a file with the same name exists in the destination directory
        if os.path.exists(dest_path):
            base, ext = os.path.splitext(filename)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            new_filename = f"{base}_{timestamp}{ext}"
            dest_path = os.path.join(dest_dir, new_filename)
            print(f"Duplicate found, renaming to: {new_filename}")

        # Move the file to the destination directory
        shutil.move(src_path, dest_path)
        print(f"Moved: {src_path} -> {dest_path}")

    except FileNotFoundError:
        print(f"File not found: {src_path}")
    except PermissionError:
        print(f"Permission denied for file: {src_path}")
    except Exception as e:
        print(f"An error occurred while moving {src_path}: {str(e)}")

# Organize and move files based on their extension
def organize_downloaded_files(download_dir):
    csv_dir, dat_dir, others_dir = create_date_directory(download_dir)

    try:
        for filename in os.listdir(download_dir):
            file_path = os.path.join(download_dir, filename)

            if os.path.isfile(file_path):
                file_extension = os.path.splitext(filename)[1].lower()

                if file_extension == '.csv':
                    # Validate CSV file before moving
                    if is_valid_csv(file_path):
                        duplicate_file_handler(file_path, csv_dir)
                    else:
                        print(f"Skipped invalid CSV file: {file_path}")
                elif file_extension == '.dat':
                    duplicate_file_handler(file_path, dat_dir)
                else:
                    duplicate_file_handler(file_path, others_dir)

    except FileNotFoundError:
        print(f"Error: The specified directory {download_dir} does not exist.")
    except PermissionError:
        print(f"Error: Permission denied when accessing {download_dir}.")
    except Exception as e:
        print(f"An error occurred while organizing the files: {str(e)}")

if _name_ == "_main_":
    download_dir = "downloads"
    organize_downloaded_files(download_dir)