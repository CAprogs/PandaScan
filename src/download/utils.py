import os
import time
import glob
import zipfile
from src.foundation.core.essentials import LOG


def check_manga_path(chapter_file_path: str):
    """Check if the manga path exists.

    Args:
        chapter_file_path (str): path of the folder where to save images

    Returns:
        bool: True(manga already exists), False(otherwise)
    """

    if not os.path.exists(chapter_file_path):
        os.makedirs(chapter_file_path)
        return False
    else:
        LOG.debug(f"Download skipped !\n\nChapter found in : {chapter_file_path}")
        return True


def set_download_path(DRIVER, path: str):
    """Set the download path.

    Args:
        DRIVER (ANY): the chromedriver
        path (str): path to the folder where to save files
    """

    try:
        params = {'behavior': 'allow', 'downloadPath': path}
        DRIVER.execute_cdp_cmd('Page.setDownloadBehavior', params)
    except Exception as e:
        LOG.debug(f"Error while setting download path : {e}")


def extract_zip(zip_file_path: str, extraction_path: str):
    """Extract the zip file.

    Args:
        zip_file_path (str): path of the zip file
        extraction_path (str): path of the folder where to extract files
    """

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extraction_path)


def find_latest_zip(chapter_file_path: str, timeout: int = 60):
    """Search for the latest zip file in the download path.

    Args:
        chapter_file_path (str): path of the folder where to save files
        timeout (int, optional): timeout in seconds. Defaults to 60.

    Returns:
        str: path of the latest zip file
    """

    start_time = time.time()

    while time.time() - start_time < timeout:
        zip_files = glob.glob(os.path.join(chapter_file_path, '*.zip'))
        if zip_files:
            return max(zip_files, key=os.path.getctime)
        time.sleep(1)
    return None
