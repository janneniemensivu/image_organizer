import os
import shutil
import unittest
from image_manager import ImageManager, manage_duplicates

class TestDuplicatesManager(unittest.TestCase):
    def setUp(self):
        self.src_folder = "test_images"
        self.dst_folder = "test_output"
        self.unknown_folder = "unknown"
        os.makedirs(os.path.join(self.dst_folder, "images", "2022"), exist_ok=True)
        os.makedirs(os.path.join(self.dst_folder, self.unknown_folder), exist_ok=True)
        shutil.copy("test_images/image1.jpg", os.path.join(self.dst_folder, "images", "2022"))
        self.image_manager = ImageManager(self.src_folder, self.dst_folder, self.unknown_folder)

    def test_manage_duplicates(self):
        img1_path = os.path.join(self.dst_folder, "images", "2022", "image1.jpg")
        img2_path = "test_images/image2.jpg"
        img3_path = "test_images/image3.jpg"

        # These should all be True
        self.assertTrue(manage_duplicates(img1_path, img1_path))
        self.assertTrue(manage_duplicates(img1_path, os.path.join(self.dst_folder, "images", "2022", "image1_1.jpg")))
        self.assertTrue(manage_duplicates(img1_path, os.path.join(self.dst_folder, self.unknown_folder, "image1.jpg")))

        # These should all be False
        self.assertFalse(manage_duplicates(img1_path, img2_path))
        self.assertFalse(manage_duplicates(img1_path, img3_path))
        self.assertFalse(manage_duplicates(img2_path, img3_path))

    def tearDown(self):
        shutil.rmtree(self.dst_folder)
