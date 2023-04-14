import os
import shutil
import unittest

from image_manager import ImageManager
from exif_reader import InvalidFileException

class TestImageManager(unittest.TestCase):

    def setUp(self):
        self.test_data_folder = os.path.join(os.getcwd(), "tests", "test_data")
        self.src_folder = os.path.join(self.test_data_folder, "source")
        self.dst_folder = os.path.join(self.test_data_folder, "destination")
        os.makedirs(self.src_folder, exist_ok=True)
        os.makedirs(self.dst_folder, exist_ok=True)

        # Create test files
        self.test_files = ["image1.jpg", "image2.jpg", "image3.jpg", "video1.mp4", "unknown_data.txt"]
        for test_file in self.test_files:
            test_file_path = os.path.join(self.src_folder, test_file)
            open(test_file_path, "w").close()

        # Create test images with EXIF data
        self.exif_test_files = ["image1.jpg", "image2.jpg", "image3.jpg"]
        for test_file in self.exif_test_files:
            test_file_path = os.path.join(self.src_folder, test_file)
            shutil.copyfile(os.path.join(self.test_data_folder, test_file), test_file_path)

        self.image_manager = ImageManager(self.src_folder, self.dst_folder)

    def test_process_image_folder(self):
        self.image_manager.process_files()

        # Check that source files have been removed
        self.assertEqual(len(os.listdir(self.src_folder)), 0)

        # Check that files have been moved to the correct destination folders
        self.assertEqual(os.listdir(self.dst_folder), ["images", "videos", "unknown"])
        self.assertEqual(os.listdir(os.path.join(self.dst_folder, "images")), ["2011", "2012"])
        self.assertEqual(os.listdir(os.path.join(self.dst_folder, "images", "2011")), ["image1.jpg"])
        self.assertEqual(os.listdir(os.path.join(self.dst_folder, "images", "2012")), ["image2.jpg", "image3.jpg"])

        # Check that invalid files have not been moved
        self.assertEqual(os.listdir(os.path.join(self.dst_folder, "videos")), ["video1.mp4"])
        self.assertEqual(os.listdir(os.path.join(self.dst_folder, "unknown")), ["unknown_data.txt"])

        # Check that the files with EXIF data have been moved correctly
        self.assertEqual(os.listdir(os.path.join(self.dst_folder, "images", "2011")), ["image1.jpg"])
        self.assertEqual(os.listdir(os.path.join(self.dst_folder, "images", "2012")), ["image2.jpg", "image3.jpg"])
        self.assertEqual(self.image_manager.exif_data, {
            "image1.jpg": {"DateTimeOriginal": "2011:05:15 12:30:00"},
            "image2.jpg": {"DateTimeOriginal": "2012:06:18 13:45:00"},
            "image3.jpg": {"DateTimeOriginal": "2012:06:18 14:00:00"}
        })

    def test_process_image_file(self):
        image_file = os.path.join(self.src_folder, "image1.jpg")
        self.image_manager.process_image_file(image_file)

        # Check that source file has been removed
        self.assertEqual(len(os.listdir(self.src_folder)), 4)

        # Check that file has been moved to the correct destination folder
        self.assertEqual(os.listdir(self.dst_folder), ["images"])
        self.assertEqual(os.listdir(os.path.join(self.dst_folder, "images")), ["2011"])
