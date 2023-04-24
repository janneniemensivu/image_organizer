import os
import shutil
import filecmp
import unittest

from file_processor import FileProcessor


class TestImageManager(unittest.TestCase):
    def setUp(self):
        # paths for test environment source and destination folders
        self.src_folder = os.path.join("tests", "source")
        self.dst_folder = os.path.join("tests", "destination")

        # create source folder
        os.makedirs(self.src_folder, exist_ok=True)

        self.test_files = {
            "image_2011": os.path.join("tests", "test_data", "image1.jpg"),
            "image_2012": os.path.join("tests", "test_data", "image2.jpg"),
            "image_2_2011": os.path.join("tests", "test_data", "image3.jpg"),
            "unknown_data": os.path.join("tests", "test_data", "unknown_data.txt"),
            "video_2013": os.path.join("tests", "test_data", "video1.mp4"),
            "video_2015": os.path.join("tests", "test_data", "video2.mp4")
        }

    def test_image_files_are_moved_to_appropriate_year_folders(self):
        # Copy test image files to source folder for testing
        shutil.copy(self.test_files["image_2011"],
                    os.path.join(self.src_folder, "image1.jpg"))
        shutil.copy(self.test_files["image_2012"],
                    os.path.join(self.src_folder, "image2.jpg"))

        # Process files
        file_processor = FileProcessor(self.src_folder, self.dst_folder)
        file_processor.process_files()

        # Check that images are moved to appropriate year folders
        self.assertTrue(os.path.exists(os.path.join(
            self.dst_folder, "images", "2011", "image1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(
            self.dst_folder, "images", "2012", "image2.jpg")))

    def test_multiple_subfolders(self):
        # Create subdirectories and test files in source directory for testing
        os.makedirs(os.path.join(self.src_folder, "folder_1"), exist_ok=True)
        os.makedirs(os.path.join(self.src_folder, "folder_2"), exist_ok=True)
        shutil.copy(self.test_files["image_2011"], os.path.join(
            self.src_folder, "folder_1", "image_1.jpg"))
        shutil.copy(self.test_files["image_2012"], os.path.join(
            self.src_folder, "folder_2", "image_2.jpg"))

        # Process files
        file_processor = FileProcessor(self.src_folder, self.dst_folder)
        file_processor.process_files()

        # Check that images are moved to appropriate year folders
        self.assertTrue(os.path.exists(os.path.join(
            self.dst_folder, "images", "2011", "image_1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(
            self.dst_folder, "images", "2012", "image_2.jpg")))

    def test_empty_folders_deletion(self):
        # Create test folders in source folder
        folder1_path = os.path.join(self.src_folder, "folder_1")
        folder2_path = os.path.join(self.src_folder, "folder_2")
        os.makedirs(folder1_path, exist_ok=True)
        os.makedirs(folder2_path, exist_ok=True)

        # Copy test image files to test folders
        shutil.copy(self.test_files["image_2011"], os.path.join(
            folder1_path, "image_2011.jpg"))
        shutil.copy(self.test_files["image_2012"], os.path.join(
            folder2_path, "image_2012.jpg"))

        # Process files
        file_processor = FileProcessor(self.src_folder, self.dst_folder)
        file_processor.process_files()

        # Check that empty folders are deleted from source
        self.assertFalse(os.path.exists(folder1_path))
        self.assertFalse(os.path.exists(folder2_path))

    def test_multiple_copies_same_file(self):
        # Create two images with the same name in different source folders
        os.makedirs(self.src_folder, exist_ok=True)

        image1_path_1 = os.path.join(self.src_folder, "folder_1", "image1.jpg")
        os.makedirs(os.path.join(self.src_folder, "folder_1"), exist_ok=True)
        shutil.copy(self.test_files["image_2011"], image1_path_1)

        image1_path_2 = os.path.join(self.src_folder, "folder_2", "image1.jpg")
        os.makedirs(os.path.join(self.src_folder, "folder_2"), exist_ok=True)
        shutil.copy(self.test_files["image_2011"], image1_path_2)

        # Process files
        file_processor = FileProcessor(self.src_folder, self.dst_folder)
        file_processor.process_files()

        # Check that there is one copy of image1.jpg in the 2011 directory
        files_in_2011 = [f for f in os.listdir(os.path.join(
            self.dst_folder, "images", "2011")) if f.endswith(".jpg")]
        self.assertEqual(len(files_in_2011), 1)

    def test_duplicate_file_renaming(self):
        # Create two images with the same name in different source folders

        os.makedirs(self.src_folder, exist_ok=True)

        image1_path = os.path.join(self.src_folder, "folder_1", "image1.jpg")
        os.makedirs(os.path.join(self.src_folder, "folder_1"), exist_ok=True)
        shutil.copy(self.test_files["image_2011"], image1_path)

        image2_path = os.path.join(self.src_folder, "folder_2", "image1.jpg")
        os.makedirs(os.path.join(self.src_folder, "folder_2"), exist_ok=True)
        shutil.copy(self.test_files["image_2_2011"], image2_path)

        # Process files
        file_processor = FileProcessor(self.src_folder, self.dst_folder)
        file_processor.process_files()

        # Check that there are two jpg files in the 2011 directory
        files_in_2011 = [f for f in os.listdir(os.path.join(
            self.dst_folder, "images", "2011")) if f.endswith(".jpg")]
        self.assertEqual(len(files_in_2011), 2)

    def test_same_filename_in_different_folders(self):
        # Create two different files with the same name in different source folders
        os.makedirs(os.path.join(self.src_folder, "folder_1"), exist_ok=True)
        shutil.copy(self.test_files["image_2011"], os.path.join(
            self.src_folder, "folder_1", "image1.jpg"))

        os.makedirs(os.path.join(self.src_folder, "folder_2"), exist_ok=True)
        shutil.copy(self.test_files["image_2012"], os.path.join(
            self.src_folder, "folder_2", "image1.jpg"))

        # Process files
        file_processor = FileProcessor(self.src_folder, self.dst_folder)
        file_processor.process_files()

        # Check that there are two jpg files in 2011 and 2012 directory respectively
        files_in_2011 = [f for f in os.listdir(os.path.join(
            self.dst_folder, "images", "2011")) if f.endswith(".jpg")]
        files_in_2012 = [f for f in os.listdir(os.path.join(
            self.dst_folder, "images", "2012")) if f.endswith(".jpg")]
        self.assertEqual(len(files_in_2011), 1)
        self.assertEqual(len(files_in_2012), 1)

        # Check that the content of both files is the same as in the original files
        original_image_2011 = self.test_files["image_2011"]
        original_image_2012 = self.test_files["image_2012"]
        copied_image_2011 = os.path.join(
            self.dst_folder, "images", "2011", "image1.jpg")
        copied_image_2012 = os.path.join(
            self.dst_folder, "images", "2012", "image1.jpg")

        self.assertTrue(filecmp.cmp(original_image_2011, copied_image_2011))
        self.assertTrue(filecmp.cmp(original_image_2012, copied_image_2012))

    def tearDown(self):
        shutil.rmtree(self.src_folder)
        shutil.rmtree(self.dst_folder)


if __name__ == "__main__":
    unittest.main()
