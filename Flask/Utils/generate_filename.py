import string
import random
import time
import os

def generate_timestamp_based_filename(original_filename, prefix=None):
    """
    Generate a filename based on the current timestamp and a random suffix.
    Keeps the filename short while ensuring uniqueness.

    Args:
        original_filename (str): The original filename to extract the extension.
        prefix (str, optional): An optional prefix to prepend to the filename.

    Returns:
        str: Generated unique filename with timestamp and random suffix.
    """
    timestamp = int(time.time())
    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    file_extension = os.path.splitext(original_filename)[1]

    unique_filename = f"{timestamp}_{random_suffix}{file_extension}"

    if prefix:
        unique_filename = f"{prefix}_{unique_filename}"

    return unique_filename
