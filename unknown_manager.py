import os
from datetime import datetime
from base_manager import BaseManager


class UnknownManager(BaseManager):
    def __init__(self, dst_folder):
        super().__init__(dst_folder)

    def process_unknown_file(self, src_path):
        self.process_unsupported_file_type(src_path)

    def process_unsupported_file_type(self, src_path):
        # dst_dir = os.path.join(self.dst_folder, 'unknown')
        dst_dir = self.dst_folder
        self.create_directory_if_not_exists(dst_dir)
        dst_path = os.path.join(dst_dir, os.path.basename(src_path))
        if os.path.exists(dst_path):
            name, ext = os.path.splitext(os.path.basename(src_path))
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"{name}_{timestamp}{ext}"
            dst_path = os.path.join(dst_dir, new_name)
        self.move_file(src_path, dst_path)
