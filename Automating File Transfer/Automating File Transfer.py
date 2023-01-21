''' You work at a company that receives daily data files from external partners. These files need to be processed and analyzed, but first, they need to be transferred to the company's internal network.

    The goal of this project is to automate the process of transferring the files from an external FTP server to the company's internal network.

    Here are the steps you can take to automate this process:

    Use the ftplib library to connect to the external FTP server and list the files in the directory.

    Use the os library to check for the existence of a local directory where the files will be stored.

    Use a for loop to iterate through the files on the FTP server and download them to the local directory using the ftplib.retrbinary() method.

    Use the shutil library to move the files from the local directory to the internal network.

    Use the schedule library to schedule the script to run daily at a specific time.

    You can also set up a log file to keep track of the files that have been transferred and any errors that may have occurred during the transfer process. '''

from ftplib import FTP
import json
import logging
import os
import schedule
import shutil
import time

DAILY_TIME = "20:00"
SRC_FOLDER = os.path.join(os.getcwd(), "src")
TEMP_FOLDER = os.path.join(os.getcwd(), ".temp")
FORMAT = "%(asctime)s : %(levelname)s - %(message)s"

logging.basicConfig(level=logging.DEBUG, format=FORMAT)

file_handler = logging.FileHandler(os.path.join(SRC_FOLDER,
                                                "File Transfer.log"))
file_handler.setFormatter(logging.Formatter(FORMAT))

logger = logging.getLogger("AFT")
logger.addHandler(file_handler)


def download(ftp, files=[], downloaded_files=[]):
    for file in files:
        try:
            if file not in downloaded_files and file not in ("frep", "input"):
                logger.info(f"Downloading {file}...")
                file_path = os.path.join(TEMP_FOLDER, file)
                ftp.retrbinary(f"RETR {file}", open(file_path, "wb").write)
                logger.info(f"Downloaded {file}.")

        except Exception as e:
            logger.exception(f"Error while trying to download {file}: {e}")


def move(destination, files=[]):
    for file in files:
        try:
            logger.info(f"Moving {file}...")
            shutil.move(os.path.join(TEMP_FOLDER, file),
                        os.path.join(destination, file))
            logger.info(f"Moved {file}.")
        except Exception as e:
            logger.exception(f"Error moving {file}: {e}")


def main():
    try:
        file = open(os.path.join(SRC_FOLDER, "settings.json"))
        data = json.load(file)

        host = data["Host"]
        user = data["User"]
        password = data["Password"]
        destination = data["DownloadFolder"]

        logger.info("Found settings file.")
    except Exception as e:
        logger.exception(f"Could not find settings file: {e}")
        return

    if not os.path.exists(destination):
        os.makedirs(destination)

    try:
        ftp = FTP(host, user, password)
        logger.info("Successfully connected to the FTP server.")
    except Exception as e:
        logger.exception(f"Failed to login: {e}")
        return

    if not os.path.exists(TEMP_FOLDER):
        os.makedirs(TEMP_FOLDER)

    try:
        files = ftp.nlst()
    except Exception as e:
        logger.exception(f"Failed to retrieve list of files: {e}")
        return

    download(ftp, files, os.listdir(destination))

    try:
        ftp.quit()
        logger.info("Successfully exited the FTP server.")
    except Exception as e:
        logger.exception("Failed to exit FTP server: {e}")
        return

    move(destination, os.listdir(TEMP_FOLDER))

    try:
        os.removedirs(TEMP_FOLDER)
        logger.info("Successfully removed temporary folder.")
    except Exception as e:
        logger.exception("Error deleting temporary folder: {e}")


schedule.every().day.at(DAILY_TIME).do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
