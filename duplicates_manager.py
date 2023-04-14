import os
import hashlib
import shutil


def generate_checksum(file_path):
    """Generate a SHA-1 hash for a file."""
    with open(file_path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()


def manage_duplicates(src_path, dst_folder):
    """Move duplicate files to the specified folder."""
    filename = os.path.basename(src_path)
    dst_path = os.path.join(dst_folder, filename)

    if os.path.exists(dst_path):
        # File already exists in the destination folder
        # Compare the checksums to see if they are the same file
        if generate_checksum(src_path) == generate_checksum(dst_path):
            # Duplicate file, delete the source file
            os.remove(src_path)
        else:
            # Different file with the same name, rename the source file before moving it
            # Use the SHA-1 hash of the file contents as the new filename
            new_filename = generate_checksum(src_path)
            new_path = os.path.join(dst_folder, new_filename)
            shutil.move(src_path, new_path)
    else:
        # File does not exist in the destination folder, move it
        shutil.move(src_path, dst_path)
