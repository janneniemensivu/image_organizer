import os
import shutil
import filecmp
from base_manager import BaseManager


class UnknownManager(BaseManager):
    def __init__(self, dst_folder):
        super().__init__(dst_folder)

    def process_file(self, src_path):
        # Set destination folder to unknown folder
        dst_folder = os.path.join(self.dst_folder, "unknown")
        os.makedirs(dst_folder, exist_ok=True)

        # Copy file to destination folder
        file_name = os.path.basename(src_path)
        dst_path = os.path.join(dst_folder, file_name)

        # If file with the same name already exists in destination directory,
        # check if they have the same content
        if os.path.exists(dst_path):
            if filecmp.cmp(src_path, dst_path):
                # If the files are the same, do not copy the file
                print(f"File {file_name} already exists in {dst_folder}. Skipping.")
                return
            else:
                # If the files are different, change the filename by appending "_duplicate" to the original filename
                file_name, extension = os.path.splitext(file_name)
                file_name = f"{file_name}_duplicate{extension}"
                dst_path = os.path.join(dst_folder, file_name)

        shutil.copy2(src_path, dst_path)
