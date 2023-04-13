import os
import shutil
from PIL import Image
import datetime
from image_manager import process_image_file
from video_manager import process_video_file
from unknown_manager import process_unknown_file
from duplicates_manager import find_duplicate_files, delete_duplicate_files

src_folder = "source"
dst_folder = "destination"
unknown_folder = "unknown"
meta_file = "metadata.txt"

# Process images, videos, and unknown files
for root, dirs, files in os.walk(src_folder):
    for file in files:
        src_path = os.path.join(root, file)
        if process_image_file(src_path, dst_folder, meta_file):
            continue
        if process_video_file(src_path, dst_folder, meta_file):
            continue
        process_unknown_file(src_path, dst_folder, unknown_folder, meta_file)

# Delete duplicate files
duplicates = find_duplicate_files(dst_folder)
delete_duplicate_files(duplicates)
