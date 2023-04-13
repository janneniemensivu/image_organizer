import unittest
import os
from video_manager import process_video_file

class TestVideoManager(unittest.TestCase):
    def test_process_video_file(self):
        src_path = "tests/sample_files/videos/video1.mp4"
        dst_dir = "tests/sample_files/destination/videos/2022"
        expected_dst_path = os.path.join(dst_dir, "video1.mp4")
        process_video_file(src_path, dst_dir)
        self.assertTrue(os.path.exists(expected_dst_path))
        os.remove(expected_dst_path)
