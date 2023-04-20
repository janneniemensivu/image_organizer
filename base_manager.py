import os
import shutil
import datetime
from exif_reader import InvalidFileException

class BaseManager:
    def __init__(self, dst_folder):
        self.dst_folder = dst_folder

    def files_have_same_content(self, src_path, dst_path):
        if os.path.exists(dst_path) and os.path.getsize(src_path) == os.path.getsize(dst_path):
            with open(src_path, 'rb') as src_file, open(dst_path, 'rb') as dst_file:
                return src_file.read() == dst_file.read()
        return False

    def create_directory_if_not_exists(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def move_file(self, src_path, dst_path):
        self.create_directory_if_not_exists(os.path.dirname(dst_path))
        shutil.move(src_path, dst_path)

    def process_file(self, src_path, year):
        print("enter process_file: " + str(src_path) + ", " + year) 
        try:
            dst_dir = os.path.join(self.dst_folder, year)
            self.create_directory_if_not_exists(dst_dir)
            dst_path = os.path.join(dst_dir, os.path.basename(src_path))
            if os.path.exists(dst_path):
                if self.files_have_same_content(src_path, dst_path):
                    os.remove(src_path)
                else:
                    name, ext = os.path.splitext(os.path.basename(src_path))
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_name = f"{name}_{timestamp}{ext}"
                    dst_path = os.path.join(dst_dir, new_name)
                    self.move_file(src_path, dst_path)
            else:
                self.move_file(src_path, dst_path)
        except InvalidFileException:
            self.handle_unsupported_file(src_path)

    def handle_unsupported_file(self, src_path):
        dst_path = os.path.join(self.dst_folder, 'unknown_year', os.path.basename(src_path))
        if self.files_have_same_content(src_path, dst_path):
            os.remove(src_path)
            return
        self.create_directory_if_not_exists(os.path.dirname(dst_path))
        self.move_file(src_path, dst_path)
