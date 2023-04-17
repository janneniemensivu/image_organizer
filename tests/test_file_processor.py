import os
import shutil
import unittest

from file_processor import FileProcessor


class TestFileProcessor(unittest.TestCase):
    def setUp(self):
        self.src_directory = os.path.join("chatGPT", "source")
        self.dst_directory = os.path.join("chatGPT", "destination")
        
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
        file_processor = FileProcessor(self.src_directory, self.dst_directory)
        file_processor.process_file(os.path.join(self.src_directory, "image1.jpg"))

        self.assertEqual(len(os.listdir(os.path.join(self.dst_directory, "images", "2011"))), 1)

    def test_process_image_folder(self):
        file_processor = FileProcessor(self.src_directory, self.dst_directory)
        file_processor.process_files()

        self.assertEqual(len(os.listdir(os.path.join(self.dst_directory, "images", "2011"))), 1)
        self.assertEqual(len(os.listdir(os.path.join(self.dst_directory, "images", "2012"))), 1)

    def test_empty_folder_deletion(self):
        # create empty folder in source directory
        empty_folder_path = os.path.join(self.src_directory, "empty_folder")
        os.makedirs(empty_folder_path, exist_ok=True)

        # process files and check that empty folder is deleted
        file_processor = FileProcessor(self.src_directory, self.dst_directory)
        file_processor.process_files()

        self.assertFalse(os.path.exists(empty_folder_path))

    def test_non_empty_folder_deletion(self):
        # create non-empty folder in source directory
        non_empty_folder_path = os.path.join(self.src_directory, "non_empty_folder")
        os.makedirs(non_empty_folder_path, exist_ok=True)
        with open(os.path.join(non_empty_folder_path, "test_file.txt"), "w") as f:
            f.write("test")

        # process files and check that non-empty folder is not deleted
        file_processor = FileProcessor(self.src_directory, self.dst_directory)

        file_processor.process_files()
        self.assertTrue(os.path.exists(non_empty_folder_path))

    def tearDown(self):
        shutil.rmtree(self.src_directory)
        shutil.rmtree(self.dst_directory)


if __name__ == "__main__":
    unittest.main()
