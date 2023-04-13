from PIL import Image, ExifTags
from datetime import datetime

def get_exif_data(image):
    try:
        exif_data = image._getexif()
        return {ExifTags.TAGS[k]: v for k, v in exif_data.items() if k in ExifTags.TAGS}
    except AttributeError:
        return None

def get_date_taken(exif_data):
    if exif_data:
        date_fields = ['DateTimeOriginal', 'DateTimeDigitized', 'DateTime']
        for field in date_fields:
            if field in exif_data:
                try:
                    date_str = exif_data[field]
                    date_obj = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                    return date_obj
                except ValueError:
                    pass
    return None
