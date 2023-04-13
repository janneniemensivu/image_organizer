import os
import shutil

def process_unknown_file(src_path, dst_folder):
    unknown_folder = "unknown"
    unknown_dir = os.path.join(dst_folder, unknown_folder)
    os.makedirs(unknown_dir, exist_ok=True)
    file = os.path.basename(src_path)
    dst_path = os.path.join(unknown_dir, file)
    shutil.move(src_path, dst_path)
    return dst_path

def move_unknown_file(src_folder, dst_folder):
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            file_path = os.path.join(root, file)
            process_unknown_file(file_path, dst_folder)
