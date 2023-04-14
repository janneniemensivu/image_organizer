import os
import shutil


def process_unknown_file(src_folder, dst_folder):
    """ Move unknown files to the specified folder. """
    dst_folder = os.path.join(dst_folder, "unknown")
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    for filename in os.listdir(src_folder):
        src_path = os.path.join(src_folder, filename)

        if os.path.isdir(src_path):
            continue

        ext = os.path.splitext(filename)[1].lower()

        if ext in {".jpg", ".jpeg", ".gif", ".png"}:
            continue

        dst_path = os.path.join(dst_folder, filename)
        shutil.move(src_path, dst_path)
