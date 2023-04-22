from exif_reader import get_date_taken
from base_manager import BaseManager


class ImageManager(BaseManager):
    def __init__(self, dst_folder):
        super().__init__(dst_folder)
        # self.src_folder = src_folder

    def process_image_file(self, src_path):
        year = str(get_date_taken(src_path).year)
        self.process_file(src_path, year)
