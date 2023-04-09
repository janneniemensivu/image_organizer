import os
import shutil
from PIL import Image
import datetime
import hashlib

src_folder = "source"
dst_folder = "destination"
unknown_folder = "unknown"
meta_file = "metadata.txt"
hash_func = hashlib.md5  # choose the hash function to use

# create a dictionary to store the file hashes
hashes = {}

with open(meta_file, "w") as f:
    f.write("filename,source path,destination path\n")

for root, dirs, files in os.walk(src_folder):
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
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

         elif file.lower().endswith((".mov", ".mp4")):
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

# walk through the destination folder and its subdirectories in reverse order
for root, dirs, files in os.walk(dst_folder, topdown=False):
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg", ".png", ".mov", ".mp4")):
            try:
                # check if the file hash is already in the dictionary
                with open(os.path.join(root, file), "rb") as f:
                    file_hash = hash_func(f.read()).hexdigest()
                if file_hash in hashes:
                    # check if the file in the destination folder is the same as the one in the source folder
                    if hashes[file_hash] == os.path.join(os.path.relpath(root, dst_folder), file):
                        continue
                    # move the file to the deleted_duplicates folder
                    deleted_dir = os.path.join(dst_folder, "deleted_duplicates")
                    os.makedirs(deleted_dir, exist_ok=True)
                    dst_path = os.path.join(deleted_dir, file)
                    shutil.move(os.path.join(root, file), dst_path)
                    with open(meta_file, "a") as f:
                        f.write(f"{file},{os.path.join(root, file)},{dst_path}\n")
                        print(f"Moved file {os.path.join(root, file)} to {dst_path}")
                else:
                    # add the file hash to the dictionary
                    hashes[file_hash] = os.path.join(os.path.relpath(root, dst_folder), file)
            except Exception as e:
                print(f"Error processing file {os.path.join(root, file)}: {e}")

        # check if a file with the same name already exists in the destination folder
        elif file.lower().endswith((".jpg", ".jpeg", ".png", ".mov", ".mp4")) and os.path.exists(os.path.join(root, file)):
            i = 1
            while True:
                new_file = f"{os.path.splitext(file)[0]}_{i}{os.path.splitext(file)[1]}"
                new_path = os.path.join(root, new_file)
                # check if the new path already exists in the destination folder
                if not os.path.exists(new_path):
                    dst_path = new_path
                    shutil.move(os.path.join(root, file), dst_path)
                    with open(meta_file, "a") as f:
                        f.write(f"{file},{os.path.join(root, file)},{dst_path}\n")
                        print(f"Moved file {os.path.join(root, file)} to {dst_path}")
                    break
                i += 1

# remove empty directories in the destination folder
for root, dirs, files in os.walk(dst_folder, topdown=False):
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        if not os.listdir(dir_path):
            os.rmdir(dir_path)
