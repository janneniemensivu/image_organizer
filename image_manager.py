import os
import shutil
from datetime import datetime
from PIL import Image
from exif_reader import get_date_taken, InvalidFileException


class ImageManager:
    def __init__(self, src_folder, dst_folder):
        self.src = src_folder
        self.dst = dst_folder

    def process_file(self, src_path):
        try:
            date = get_date_taken(src_path)
            year_folder = str(date.year)
            dst_folder = os.path.join(self.dst, "images", year_folder)
            if not os.path.exists(dst_folder):
                os.makedirs(dst_folder)
            shutil.move(src_path, os.path.join(dst_folder, os.path.basename(src_path)))
        except InvalidFileException:
            pass  # ignore invalid files
