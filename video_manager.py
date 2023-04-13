import os
import shutil
import datetime


def process_video_file(src_path, dst_folder):
    """
    Processes a video file, moving it to the appropriate year folder in the videos directory
    based on the file's modification date.
    """
    try:
        year = datetime.datetime.fromtimestamp(os.path.getmtime(src_path)).strftime('%Y')
        dst_dir = os.path.join(dst_folder, "videos", year)
        os.makedirs(dst_dir, exist_ok=True)
        dst_path = os.path.join(dst_dir, os.path.basename(src_path))
        shutil.move(src_path, dst_path)
        print(f"Moved file {src_path} to {dst_path}")
        return dst_path
    except Exception as e:
        print(f"Error processing file {src_path}: {e}")
        return None


def process_video_folder(src_folder, dst_folder):
    """
    Processes a folder containing video files, moving each file to the appropriate year folder
    in the videos directory based on the file's modification date.
    """
    for root, dirs, files in os.walk(src_folder):
        for file in files:
            if file.endswith(".mov") or file.endswith(".MOV") or file.endswith(".mp4") or file.endswith(".MP4"):
                src_path = os.path.join(root, file)
                process_video_file(src_path, dst_folder)


if __name__ == "__main__":
    src_folder = "source"
    dst_folder = "destination"
    process_video_folder(src_folder, dst_folder)
