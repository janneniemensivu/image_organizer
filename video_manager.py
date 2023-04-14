import os
import shutil


def process_video_file(src_path, dst_folder):
    """ Move video files to the specified folder. """
    filename = os.path.basename(src_path)
    dst_folder = os.path.join(dst_folder, "videos")

    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    dst_path = os.path.join(dst_folder, filename)
    shutil.move(src_path, dst_path)
