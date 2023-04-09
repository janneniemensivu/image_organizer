import os
import shutil
from PIL import Image
import datetime

src_folder = "source"
dst_folder = "destination"
unknown_folder = "unknown"
meta_file = "metadata.txt"

with open(meta_file, "w") as f:
    f.write("filename,source path,destination path\n")

for root, dirs, files in os.walk(src_folder):
    for file in files:
        if file.endswith(".jpg") or file.endswith(".JPG") or file.endswith(".jpeg") or file.endswith(".JPEG"):
            try:
                src_path = os.path.join(root, file)
                with Image.open(src_path) as im:
                    exif_data = im.getexif()
                if exif_data:
                    date_info = exif_data.get(306)
                    if date_info:
                        year = date_info[:4]
                        dst_dir = os.path.join(dst_folder, "images", year)
                        os.makedirs(dst_dir, exist_ok=True)
                        dst_path = os.path.join(dst_dir, file)
                        shutil.move(src_path, dst_path)
                        with open(meta_file, "a") as f:
                            f.write(f"{file},{src_path},{dst_path}\n")
                            print(f"Moved file {src_path} to {dst_path}")
                else:
                    print(f"No exif data found in file {src_path}")
                    unknown_dir = os.path.join(dst_folder, unknown_folder)
                    os.makedirs(unknown_dir, exist_ok=True)
                    dst_path = os.path.join(unknown_dir, file)
                    shutil.move(src_path, dst_path)
                    with open(meta_file, "a") as f:
                        f.write(f"{file},{src_path},{dst_path}\n")
                        print(f"Moved file {src_path} to {dst_path}")
            except Exception as e:
                print(f"Error processing file {src_path}: {e}")
                unknown_dir = os.path.join(dst_folder, unknown_folder)
                os.makedirs(unknown_dir, exist_ok=True)
                dst_path = os.path.join(unknown_dir, file)
                shutil.move(src_path, dst_path)
                with open(meta_file, "a") as f:
                    f.write(f"{file},{src_path},{dst_path}\n")
                    print(f"Moved file {src_path} to {dst_path}")
                    
        elif file.endswith(".mov") or file.endswith(".MOV") or file.endswith(".mp4") or file.endswith(".MP4"):
            try:
                src_path = os.path.join(root, file)
                year = datetime.datetime.fromtimestamp(os.path.getmtime(src_path)).strftime('%Y')
                dst_dir = os.path.join(dst_folder, "videos", year)
                os.makedirs(dst_dir, exist_ok=True)
                dst_path = os.path.join(dst_dir, file)
                shutil.move(src_path, dst_path)
                with open(meta_file, "a") as f:
                    f.write(f"{file},{src_path},{dst_path}\n")
                    print(f"Moved file {src_path} to {dst_path}")
            except Exception as e:
                print(f"Error processing file {src_path}: {e}")
                unknown_dir = os.path.join(dst_folder, unknown_folder)
                os.makedirs(unknown_dir, exist_ok=True)
                dst_path = os.path.join(unknown_dir, file)
                shutil.move(src_path, dst_path)
                with open(meta_file, "a") as f:
                    f.write(f"{file},{src_path},{dst_path}\n")
                    print(f"Moved file {src_path} to {dst_path}")

for root, dirs, files in os.walk(src_folder, topdown=False):
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        if not os.listdir(dir_path):
            os.rmdir(dir_path)
