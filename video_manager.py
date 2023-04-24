import os
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from base_manager import BaseManager


class VideoManager(BaseManager):
    def __init__(self, dst_folder):
        super().__init__(dst_folder)
        # self.src_folder = src_folder

    def get_creation_date(self, src_path):
        parser = createParser(src_path)
        if not parser:
            return None

        try:
            metadata = extractMetadata(parser)
        except Exception as e:
            print(f"Error extracting metadata from {src_path}: {e}")
            return None

        if metadata and metadata.has("creation_date"):
            return metadata.get("creation_date")
        else:
            return None

    def process_video_file(self, src_path):
        creation_date = self.get_creation_date(src_path)

        if creation_date:
            year = str(creation_date.year)
            self.process_file(src_path, year)
        else:
            self.handle_unsupported_file(src_path)
