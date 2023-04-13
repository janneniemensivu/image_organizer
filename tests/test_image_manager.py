import os
import shutil
import unittest
from image_manager import ImageManager

class TestImageManager(unittest.TestCase):
    def setUp(self):
        self.src_folder = "tests/tests_source"
        self.dst_folder = "tests/tests_destination"
        self.unknown_folder = "tests/tests_destination/unknown"

        # Create necessary folders
        os.makedirs(self.src_folder, exist_ok=True)
        os.makedirs(self.dst_folder, exist_ok=True)
        os.makedirs(os.path.join(self.dst_folder, "images"), exist_ok=True)
        os.makedirs(os.path.join(self.dst_folder, "videos"), exist_ok=True)
        os.makedirs(os.path.join(self.dst_folder, "unknown"), exist_ok=True)

        # Copy test files to source folder
        src_files = os.listdir("tests/test_data")
        for file in src_files:
            src_path = os.path.join("tests/test_data", file)
            dst_path = os.path.join(self.src_folder, file)
            shutil.copy(src_path, dst_path)
        print("src_initial_after setup: " + str(os.listdir(self.src_folder)))

        self.image_manager = ImageManager(self.src_folder, self.dst_folder, self.unknown_folder)



    def tearDown(self):
        if os.path.isdir(self.src_folder):
            shutil.rmtree(self.src_folder)
        if os.path.isdir(self.dst_folder):
            shutil.rmtree(self.dst_folder)

    def test_process_image_folder(self):
        self.image_manager.process_files()
        #print("src_initial: " + str(os.listdir(self.src_folder)))
        #print("src_processed: " + str(os.listdir(self.src_folder)))
        #print("dst: " + str(os.listdir(self.dst_folder)))
        #print("images: " + str(os.listdir(os.path.join(self.dst_folder, "images"))))

        self.assertTrue(os.path.exists(os.path.join(self.dst_folder, "images", "2011", "image1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.dst_folder, "images", "2012", "image2.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.dst_folder, "videos", "2013", "video1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.dst_folder, self.unknown_folder, "image3.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.dst_folder, self.unknown_folder, "unknown_file.txt")))


if __name__ == "__main__":
    unittest.main()
