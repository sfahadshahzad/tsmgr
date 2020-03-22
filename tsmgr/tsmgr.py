"""
tsmgr.py
https://github.com/sam210723/tsmgr

MPEG transport stream manager for broadcast monitoring systems
"""

import configparser
import os
import shutil
from channel import Channel

config = configparser.ConfigParser()
channels = {}

def init():
    print("Starting tsmgr...\n")

    # Detect FFmpeg
    detect_deps()

    # Load configuration file
    config.read('tsmgr\\tsmgr.ini')

    # Setup 
    setup_channels()


def setup_channels():
    """
    Setup channel encoders
    """
    global channels

    # Get list of channel config files
    configs = os.listdir('tsmgr/channels')

    for c in configs:
        # Parse channel config
        chan_config = configparser.ConfigParser()
        chan_config.read(f'tsmgr/channels/{c}')
        id = chan_config.get('channel', 'id')

        # Create new channel object
        channels[id] = Channel(chan_config, config)


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
