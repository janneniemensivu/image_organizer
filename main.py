import os
from image_manager import ImageManager

def main():
    src_folder = os.path.join("source")
    dst_folder = os.path.join("destination")

    image_manager = ImageManager(src_folder, dst_folder)
    image_manager.process_files()

if __name__ == "__main__":
    main()