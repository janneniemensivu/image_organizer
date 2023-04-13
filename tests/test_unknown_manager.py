import unittest
import os
from unknown_manager import process_unknown_file

class TestUnknownManager(unittest.TestCase):

    def setUp(self):
        self.test_file_path = "tests/test_files/unknown/sample_file.txt"
        self.dst_folder = "tests/destination/unknown"
        os.makedirs(self.dst_folder, exist_ok=True)

    def tearDown(self):
        os.remove(os.path.join(self.dst_folder, "sample_file.txt"))

    def test_process_unknown_file(self):
        process_unknown_file(self.test_file_path, self.dst_folder)
        self.assertTrue(os.path.exists(os.path.join(self.dst_folder, "sample_file.txt")))

if __name__ == '__main__':
    unittest.main()
