import os
import shutil
import unittest

from image_manager import ImageManager
from exif_reader import InvalidFileException
from PIL import Image


class TestImageManager(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.src_directory = os.path.join("chatGPT", "source")
        self.dst_directory = os.path.join("chatGPT", "destination")
        
    def setUp(self):
        test_files = ['image1.jpg', 'image2.jpg', 'image3.jpg', 'unknown_data.txt', 'video1.mp4']

        # create source and destination directories
        os.makedirs(self.src_directory, exist_ok=True)
        os.makedirs(os.path.join(self.dst_directory, "images"), exist_ok=True)
        os.makedirs(os.path.join(self.dst_directory, "unknown"), exist_ok=True)
        os.makedirs(os.path.join(self.dst_directory, "videos"), exist_ok=True)

        # move test files to source directory
        for filename in test_files:
            src_path = os.path.join("tests", "test_data", filename)
            dst_path = os.path.join(self.src_directory, filename)
            shutil.copy(src_path, dst_path)

    def test_process_image_file(self):
        image_manager = ImageManager(self.src_directory, self.dst_directory)
        image_manager.process_image_file(os.path.join(self.src_directory, "image1.jpg"))

        self.assertEqual(len(os.listdir(os.path.join(self.dst_directory, "images", "2011"))), 1)

    def test_process_image_folder(self):
        image_manager = ImageManager(self.src_directory, self.dst_directory)
        image_manager.process_files()

        self.assertEqual(len(os.listdir(os.path.join(self.dst_directory, "images", "2011"))), 1)
        self.assertEqual(len(os.listdir(os.path.join(self.dst_directory, "images", "2012"))), 1)

    def tearDown(self):
        shutil.rmtree(self.src_directory)
        shutil.rmtree(self.dst_directory)


if __name__ == "__main__":
    unittest.main()
