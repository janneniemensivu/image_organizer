import os


class BaseManager:
    def __init__(self, src_folder, dst_folder):
        self.src_folder = src_folder
        self.dst_folder = dst_folder

    def get_dst_path(self, src_path):
        """
        Returns the destination path for the given source path.
        """
        file_name = os.path.basename(src_path)
        dst_path = os.path.join(self.dst_folder, file_name)

        # If file with the same name already exists in destination directory,
        # rename the file by appending a number to the filename
        counter = 1
        while os.path.exists(dst_path):
            file_name, extension = os.path.splitext(file_name)
            file_name = f"{file_name}_{counter}{extension}"
            dst_path = os.path.join(self.dst_folder, file_name)
            counter += 1

        return dst_path

    def create_dst_folders(self, dst_path):
        """
        Creates the necessary folder structure in the destination folder for the
        given file path.
        """
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    def process_file(self, src_path):
        """
        Processes a file and moves it to the appropriate location in the
        destination folder.
        """
        raise NotImplementedError("process_file method must be implemented in derived classes")
