import os
from file_processor import FileProcessor

#src_folder = os.path.join("chatGPT", "source")
#dst_folder = os.path.join("chatGPT", "destination")
src_folder = "source"
dst_folder = "destination"

if __name__ == "__main__":
    file_processor = FileProcessor(src_folder, dst_folder)
    file_processor.process_files()
