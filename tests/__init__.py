import unittest
from tests.test_image_manager import TestImageManager
from tests.test_video_manager import TestVideoManager
from tests.test_unknown_manager import TestUnknownManager
from tests.test_duplicates_manager import TestDuplicatesManager

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestImageManager))
    suite.addTest(unittest.makeSuite(TestVideoManager))
    suite.addTest(unittest.makeSuite(TestUnknownManager))
    suite.addTest(unittest.makeSuite(TestDuplicatesManager))
    runner = unittest.TextTestRunner()
    runner.run(suite)
