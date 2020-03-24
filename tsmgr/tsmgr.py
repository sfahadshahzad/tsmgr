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
cli_thread = None

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

    # Setup CLI thread
    global cli_thread
    cli_thread = threading.Thread()
    cli_thread.name = "cli"
    cli_thread.daemon = True
    cli_thread.run = cli
    cli_thread.start()

    # Monitor threads
    while True:
        for t in threads:
            if not threads[t].is_alive():
                threads[t] = threading.Thread()
                threads[t].name = t
                threads[t].run = channels[t].run
                threads[t].start()
        time.sleep(5)


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

        # Check for channel ID conflicts
        try:
            channels[id]
            print(f"Channel ID conflict (ID: {id})\nExiting...")
            exit(1)
        except KeyError:
            # Create new channel object
            channels[id] = Channel(chan_config, config)

        print()
    print("--------------------------------\n")


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
    
    time.sleep(0.5)
    print()


def stop_channels():
    """
    Stop channel encoders
    """

    # Stop subprocesses
    for c in channels:
        channels[c].stop()
    
    # Wait for threads to terminate
    while True:
        alive = False
        for t in threads:
            alive |= threads[t].is_alive()
        
        if not alive: return
        time.sleep(0.1)


def cli():
    """
    Listen for and handle stdin
    """

    while True:
        try:
            i = input()
        except EOFError:
            continue
        
        print(i)


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
    stop_channels()
    print("\nExiting tsmgr...")
    exit(0)
