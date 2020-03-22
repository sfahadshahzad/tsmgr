"""
tsmgr.py
https://github.com/sam210723/tsmgr

MPEG transport stream manager for broadcast monitoring systems
"""

import configparser
import os
import shutil
import time

from channel import Channel

config = configparser.ConfigParser()
channels = {}

def init():
    print("Starting tsmgr...\n")

    # Detect FFmpeg
    detect_deps()

    # Load configuration file
    config.read('tsmgr\\tsmgr.ini')

    # Create channels objects
    create_channels()

    # Setup channel encoders
    for c in channels:
        channels[c].setup()
    
    # Run channel encoders
    for c in channels:
        channels[c].run()
    
    while True:
        time.sleep(1)


def create_channels():
    """
    Create channel objects
    """
    global channels

    # Get list of channel config files
    configs = os.listdir('tsmgr/channels')

    for c in configs:
        if not c.endswith('.ini'): continue
        
        # Parse channel config
        chan_config = configparser.ConfigParser()
        chan_config.read(f'tsmgr/channels/{c}')
        id = chan_config.get('channel', 'id')

        # Create new channel object
        channels[id] = Channel(chan_config, config)
        print()


def stop():
    """
    Stop channel encoders
    """

    for c in channels:
        channels[c].stop()


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
    print("\nExiting...")
    stop()
    exit(0)
