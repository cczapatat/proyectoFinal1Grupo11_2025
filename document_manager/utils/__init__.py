import os
from datetime import datetime


def get_extension(full_file_name: str) -> str:
    _, file_extension = os.path.splitext(full_file_name)
    extension = file_extension.replace('.', '')

    return extension


def get_base_path() -> str:
    date = datetime.now().strftime("%Y/%m/%d")

    return date
