"""
tsmgr.py
https://github.com/sam210723/tsmgr

MPEG transport stream manager for broadcast monitoring systems
"""

import configparser
import os
import shutil
import threading
import time

from channel import Channel

config = configparser.ConfigParser()
channels = {}
threads = {}

def init():
    print("Starting tsmgr...\n")

    # Detect FFmpeg
    detect_deps()

    # Load configuration file
    config.read('tsmgr\\tsmgr.ini')

    # Create, setup and run channels objects
    create_channels()
    setup_channels()
    run_channels()
    
    while True:
        # Check at least one thread is alive
        alive = False
        for t in threads:
            alive |= threads[t].is_alive()
        
        if not alive:
            print("\nNo alive threads\nExiting...")
            return

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


def setup_channels():
    """
    Setup channel object instances
    """

    # Setup channel encoders
    for c in channels:
        channels[c].setup()
    print()


def run_channels():
    """
    Create and start channel encoders
    """

    # Run channel encoders
    for c in channels:
        threads[c] = threading.Thread()
        threads[c].name = c
        threads[c].run = channels[c].run
        threads[c].start()


def stop_channels():
    """
    Stop channel encoders
    """

    # Stop subprocesses
    for c in channels:
        channels[c].stop()
    print()
    
    print("Waiting for threads to terminate...")
    while True:
        alive = False
        for t in threads:
            alive |= threads[t].is_alive()
        
        if not alive: return
        time.sleep(0.1)


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
    print("\nStopping subprocesses...")
    stop_channels()
    print("\nExiting...")
    exit(0)
