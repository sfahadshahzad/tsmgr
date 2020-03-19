"""
tsmgr.py
https://github.com/sam210723/tsmgr

MPEG transport stream manager for broadcast monitoring systems
"""

import configparser
import os
import shutil
from channel import Channel

config = None
channels = {}

def init():
    print("Starting tsmgr...\n")

    # Detect FFmpeg
    detect_deps()

    # Load configuration file
    load_config()

    # Setup 
    setup_channels()


def setup_channels():
    """
    Setup channel encoders
    """
    global channels

    # Get list of channel config files
    ch_cfgs = os.listdir('tsmgr/channels')

    for c in ch_cfgs:
        # Parse channel config
        config = configparser.ConfigParser()
        config.read(f'tsmgr/channels/{c}')
        num = config.get('channel', 'num')

        # Create new channel object
        channels[num] = Channel(config)


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
