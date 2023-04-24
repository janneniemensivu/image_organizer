from exif_reader import get_date_taken
from base_manager import BaseManager
from unknown_manager import UnknownManager


class ImageManager(BaseManager):
    def __init__(self, dst_folder):
        super().__init__(dst_folder)

    def process_image_file(self, src_path):
        try:
            year = str(get_date_taken(src_path).year)
            self.process_file(src_path, year)
        except:
            unknown_manager = UnknownManager(self.dst_folder)
            unknown_manager.process_unknown_file(src_path)
