import os
import shutil
import filecmp
import unittest
from datetime import datetime

from file_processor import FileProcessor


class TestVideoManager(unittest.TestCase):
    def setUp(self):
        # paths for test environment source and destination folders
        self.src_folder = os.path.join("tests", "source")
        self.dst_folder = os.path.join("tests", "destination")

        # create source folder
        os.makedirs(self.src_folder, exist_ok=True)

        self.test_files = {
            "video_2012": os.path.join("tests", "test_data", "video1.mp4"),
            "video_2015": os.path.join("tests", "test_data", "video2.mp4"),
        }

    def test_video_files_are_moved_to_appropriate_year_folders(self):
        # Copy test video files to source folder for testing
        shutil.copy(self.test_files["video_2012"],
                    os.path.join(self.src_folder, "video1.mp4"))
        shutil.copy(self.test_files["video_2015"],
                    os.path.join(self.src_folder, "video2.mp4"))

        # Process files
        file_processor = FileProcessor(self.src_folder, self.dst_folder)
        file_processor.process_files()

        # Check that videos are moved to appropriate year folders
        self.assertTrue(os.path.exists(os.path.join(
            self.dst_folder, "videos", "2012", "video1.mp4")))
        self.assertTrue(os.path.exists(os.path.join(
            self.dst_folder, "videos", "2015", "video2.mp4")))

    def test_duplicate_video_renaming(self):
        # Create two videos with the same name in different source folders
        os.makedirs(os.path.join(self.src_folder, "folder_1"), exist_ok=True)
        shutil.copy(self.test_files["video_2012"], os.path.join(
            self.src_folder, "folder_1", "video1.mp4"))

        os.makedirs(os.path.join(self.src_folder, "folder_2"), exist_ok=True)
        shutil.copy(self.test_files["video_2015"], os.path.join(
            self.src_folder, "folder_2", "video1.mp4"))

        # Process files
        file_processor = FileProcessor(self.src_folder, self.dst_folder)
        file_processor.process_files()

        # Check that there are two mp4 files in 2012 and 2015 directories respectively
        files_in_2012 = [f for f in os.listdir(os.path.join(
            self.dst_folder, "videos", "2012")) if f.endswith(".mp4")]
        files_in_2015 = [f for f in os.listdir(os.path.join(
            self.dst_folder, "videos", "2015")) if f.endswith(".mp4")]
        self.assertEqual(len(files_in_2012), 1)
        self.assertEqual(len(files_in_2015), 1)

        # Check that the content of both files is the same as in the original files
        original_video_2012 = self.test_files["video_2012"]
        original_video_2015 = self.test_files["video_2015"]
        copied_video_2012 = os.path.join(
            self.dst_folder, "videos", "2012", "video1.mp4")
        copied_video_2015 = os.path.join(
            self.dst_folder, "videos", "2015", "video1.mp4")

        self.assertTrue(filecmp.cmp(original_video_2012, copied_video_2012))
        self.assertTrue(filecmp.cmp(original_video_2015, copied_video_2015))

    def tearDown(self):
        shutil.rmtree(self.src_folder)
        shutil.rmtree(self.dst_folder)
