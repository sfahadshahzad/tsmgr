"""
tsmgr.py
https://github.com/sam210723/tsmgr

MPEG transport stream manager for broadcast monitoring systems
"""

import shutil


def init():
    print("Starting tsmgr...\n")

    # Detect FFmpeg
    detect_deps()


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
