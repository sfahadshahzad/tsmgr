"""
tsmgr.py
https://github.com/sam210723/tsmgr

MPEG transport stream manager for broadcast monitoring systems
"""

import configparser
import shutil

config = None

def init():
    print("Starting tsmgr...\n")

    # Detect FFmpeg
    detect_deps()

    # Load configuration file
    load_config()


def load_config():
    """
    Load configuration from INI file
    """
    global config

    config = configparser.ConfigParser()
    config.read('tsmgr.ini')


def detect_deps():
    """
    Check for FFmpeg
    """

    if shutil.which("ffmpeg") is None:
        print("FFmpeg not found")
        exit(1)


try:
    init()
except KeyboardInterrupt:
    print("Exiting...")
    exit(0)
