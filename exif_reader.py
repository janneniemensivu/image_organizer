from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
from datetime import datetime


class InvalidFileException(Exception):
    pass


def get_exif_data(image):
    """ Get the EXIF data from an image. """
    exif_data = {}
    try:
        info = image._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exif_data[decoded] = value
    except (AttributeError, KeyError, IndexError):
        pass
    return exif_data


def get_date_taken(file_path):
    """ Get the date/time that the photo was taken. """
    try:
        with Image.open(file_path) as img:
            exif_data = get_exif_data(img)
            if not exif_data:
                raise InvalidFileException("Invalid or missing EXIF data")
            date_time = exif_data.get('DateTimeOriginal') or exif_data.get('DateTime')
            if date_time:
                return datetime.strptime(date_time, '%Y:%m:%d %H:%M:%S')
            else:
                raise InvalidFileException("Invalid or missing date/time")
    except (OSError, InvalidFileException):
        raise InvalidFileException("Invalid or unsupported file type")
