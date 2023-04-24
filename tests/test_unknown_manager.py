import os
import shutil
import unittest

from file_processor import FileProcessor


class TestUnknownManager(unittest.TestCase):

    def setUp(self):
        # paths for test environment source and destination folders
        self.src_folder = os.path.join("tests", "source")
        self.dst_folder = os.path.join("tests", "destination")

        # create source folder
        os.makedirs(self.src_folder, exist_ok=True)

        # define the test files
        self.test_files = {
            "unknown_1": os.path.join("tests", "test_data", "unknown_1.txt"),
            "unknown_2": os.path.join("tests", "test_data", "unknown_2.txt"),
            "unknown_3": os.path.join("tests", "test_data", "unknown_3.txt"),
            "unknown_4": os.path.join("tests", "test_data", "unknown_4.txt"),
            "unknown_4_duplicate": os.path.join("tests", "test_data", "unknown_4_duplicate.txt"),
        }

    def test_unknown_directory_creation(self):
        # Copy test files to the source folder
        shutil.copy(self.test_files["unknown_1"], self.src_folder)

        # Process files
        file_processor = FileProcessor(self.src_folder, self.dst_folder)
        file_processor.process_files()

        # Check that the 'unknown' directory is created in the destination folder
        self.assertTrue(os.path.exists(
            os.path.join(self.dst_folder, 'unknown')))

    def test_unknown_files_moved(self):
        # Copy test files to the source folder for testing
        shutil.copy(self.test_files["unknown_1"],
                    os.path.join(self.src_folder, "file1.txt"))
        shutil.copy(self.test_files["unknown_2"],
                    os.path.join(self.src_folder, "file2.txt"))
        shutil.copy(self.test_files["unknown_3"],
                    os.path.join(self.src_folder, "file3.txt"))

        # Process files
        file_processor = FileProcessor(self.src_folder, self.dst_folder)
        file_processor.process_files()

        # Check that unknown files are moved to the 'unknown' directory
        unknown_folder = os.path.join(self.dst_folder, 'unknown')
        self.assertTrue(os.path.exists(
            os.path.join(unknown_folder, 'file1.txt')))
        self.assertTrue(os.path.exists(
            os.path.join(unknown_folder, 'file2.txt')))
        self.assertTrue(os.path.exists(
            os.path.join(unknown_folder, 'file3.txt')))

    def test_same_name_different_content(self):
        # Create a new folder and copy the file unknown_1.txt to it
        new_folder = os.path.join(self.src_folder, "new_folder")
        os.makedirs(new_folder, exist_ok=True)
        shutil.copy(self.test_files["unknown_1"], new_folder)

        # Rename unknown_2.txt to have the same name as unknown_2.txt
        shutil.copy(self.test_files["unknown_2"], self.src_folder)
        os.rename(os.path.join(self.src_folder,
                  "unknown_2.txt"), os.path.join(self.src_folder, "unknown_1.txt"))

        # Process files
        file_processor = FileProcessor(self.src_folder, self.dst_folder)
        file_processor.process_files()

        unknown_folder = os.path.join(self.dst_folder, 'unknown')

        # Check if there are two files in the 'unknown' folder with the same content as the original files
        unknown_files = [f for f in os.listdir(unknown_folder) if os.path.isfile(
            os.path.join(unknown_folder, f))]
        self.assertEqual(len(unknown_files), 2)
        self.assertNotEqual(str(unknown_files[0]), str(unknown_files[1]))

    def test_same_name_same_content(self):
        # Create a new file with the same content as unknown_file1 and the same name
        with open(os.path.join(self.src_folder, "unknown1_duplicate.txt"), "w") as f:
            f.write("This is an unknown file 1.")
        os.rename(os.path.join(self.src_folder, "unknown1_duplicate.txt"),
                  os.path.join(self.src_folder, "unknown1.txt"))

        # Process files
        file_processor = FileProcessor(self.src_folder, self.dst_folder)
        file_processor.process_files()

        # Check if there are still only three files in the 'unknown' folder
        unknown_folder = os.path.join(self.dst_folder, 'unknown')
        files = [f for f in os.listdir(unknown_folder) if os.path.isfile(
            os.path.join(unknown_folder, f))]
        self.assertEqual(len(files), 3)

    def tearDown(self):
        # Remove the source and destination folders
        shutil.rmtree(self.src_folder)
        shutil.rmtree(self.dst_folder)
