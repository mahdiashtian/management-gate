import os

from django.utils.crypto import get_random_string


def random_string(length=18):
    return get_random_string(length)


def get_file_name(file_name):
    """
    _Get File Name_
    Args:
        file_name (_str_): Name file (image,movie and ...)
    Returns:
        _tuple_: Name and ext
    """

    base_name = os.path.basename(file_name)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance=None, filename=None):
    """
    _Upload Image Path_
    Args:
        instance (django obj instance, optional): The object that the file is for. Defaults to None.
        filename (_type_, optional): The final generated name for the file. Defaults to None.
    Returns:
        _str_: Final path and file name
    """

    model_name = instance.__class__.__name__.lower()
    name, ext = get_file_name(filename)
    return f"{model_name}/{random_string()}/{name}{ext}"
