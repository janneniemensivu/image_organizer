import os
from PIL import UnidentifiedImageError
from PIL import Image
import shutil
from exif_reader import get_exif_data, get_date_taken
from duplicates_manager import manage_duplicates

class ImageManager:
    def __init__(self, src_folder, dst_folder, unknown_folder):
        self.src_folder = src_folder
        self.dst_folder = dst_folder
        self.unknown_folder = unknown_folder
        self.image_extensions = [".jpg", ".jpeg"]
        self.image_folder = "images"

    def process_files(self):
        for root, dirs, files in os.walk(self.src_folder):
            for file in files:
                if file.lower().endswith(tuple(self.image_extensions)):
                    src_path = os.path.join(root, file)
                    self.process_image_file(src_path)

    def process_image_file(self, src_path):
        try:
            image = Image.open(src_path)
            exif_data = get_exif_data(image)
            date = get_date_taken(exif_data)
            if date:
                year = str(date.year)
                # Check if the file is an image file
                if image.format:
                    file_type = image.format.lower()
                    if file_type in self.image_extensions:
                        # Create necessary folders
                        os.makedirs(os.path.join(self.dst_folder, self.image_folder, year), exist_ok=True)
                        dst_path = os.path.join(self.dst_folder, self.image_folder, year, os.path.basename(src_path))
                        shutil.copy(src_path, dst_path)
                        return True
            # If date not found or file is not an image file, move it to unknown folder
            dst_path = os.path.join(self.unknown_folder, os.path.basename(src_path))

            manage_duplicates(self.dst_folder, os.path.join(self.unknown_folder, os.path.basename(src_path)))
            return False
        except UnidentifiedImageError:
            manage_duplicates(self.dst_folder, os.path.join(self.unknown_folder, os.path.basename(src_path)))
            return False

