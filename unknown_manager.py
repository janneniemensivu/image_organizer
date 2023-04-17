import os
import shutil


class UnknownManager:
    def __init__(self, src_folder, dst_folder):
        self.src = src_folder
        self.dst = dst_folder

    def process_file(self, src_path):
        dst_folder = os.path.join(self.dst, "unknown")
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        shutil.move(src_path, os.path.join(dst_folder, os.path.basename(src_path)))
