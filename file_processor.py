import os
from image_manager import ImageManager
from video_manager import VideoManager
from unknown_manager import UnknownManager


class FileProcessor:
    def __init__(self, src_folder, dst_folder):
        self.src_folder = src_folder
        self.dst_folder = dst_folder

    def process_files(self):
        # Process all files in the source directory
        for subdir, dirs, files in os.walk(self.src_folder):
            for file in files:
                src_path = os.path.join(subdir, file)
                self.process_file(src_path)

        # Delete empty directories in the source directory
        self.delete_empty_dirs(self.src_folder)

    def process_file(self, src_path):
        file_type = self.get_file_type(src_path)

        if file_type == "image":
            manager = ImageManager(self.src_folder, self.dst_folder)
        elif file_type == "video":
            manager = VideoManager(self.src_folder, self.dst_folder)
        else:
            manager = UnknownManager(self.src_folder, self.dst_folder)

        manager.process_file(src_path)

    def get_file_type(self, src_path):
        extension = os.path.splitext(src_path)[1].lower()

        if extension in [".jpg", ".jpeg", ".png", ".gif"]:
            return "image"
        elif extension in [".mp4", ".mov", ".avi"]:
            return "video"
        else:
            return "unknown"

    def delete_empty_dirs(self, folder):
        # Delete empty directories in the specified folder
        for subdir, dirs, files in os.walk(folder, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(subdir, dir)
                try:
                    os.rmdir(dir_path)
                except OSError:
                    pass
