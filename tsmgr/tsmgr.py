"""
tsmgr.py
https://github.com/sam210723/tsmgr

MPEG transport stream manager for broadcast monitoring systems
"""

import configparser
import os
import shutil
import subprocess
import threading
import time

from channel import Channel

config = configparser.ConfigParser()
table_ver = "-1"
channels = {}
threads = {}
cli_thread = None
merge_thread = None

def init():
    print("Starting tsmgr...")

    # Detect FFmpeg
    detect_deps()

    # Load configuration file
    config.read('tsmgr\\tsmgr.ini')
    global table_ver
    table_ver = config.get('tsmgr', 'table_version')
    print(f"MPEG-TS Table Version: {table_ver}\n")

    # Create, setup and run channels objects
    create_channels()

    # Setup merge thread
    global merge_thread
    merge_thread = threading.Thread()
    merge_thread.name = "merge"
    merge_thread.daemon = True
    merge_thread.run = merge
    merge_thread.start()

    # Setup and run channel encoders
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
        time.sleep(10)


def create_channels(only_id=None):
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

        if only_id:
            if id == only_id:
                channels[id] = Channel(chan_config, config)
                print()
        else:
            # Check for channel ID conflicts
            try:
                channels[id]
                print(f"Channel ID conflict (ID: {id})\nExiting...")
                exit(1)
            except KeyError:
                # Create new channel object
                channels[id] = Channel(chan_config, config)
            print()
    if not only_id: print("--------------------------------\n")


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
    print()
    
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
        
        if i.startswith("r "):  # Reload channel
            reload_channel(i[2:])
        else:
            print("Invalid command\n")


def reload_channel(c):
    """
    Reload channel encoder 
    """

    # Check channel ID is valid
    try:
        channels[c]
    except KeyError:
        print("Invalid channel ID\n")
        return
    
    # Reload tsmgr configuration file
    config.read('tsmgr\\tsmgr.ini')
    global table_ver
    new_table_ver = config.get('tsmgr', 'table_version')
    if table_ver != new_table_ver:
        print(f"MPEG-TS Table Version: {table_ver} -> {new_table_ver}")
        table_ver = new_table_ver

    # Stop channel thread
    if threads[c].is_alive():
        channels[c].stop()
        time.sleep(1)
        print()
    
    # Create new channel object
    channels[c] == None
    create_channels(c)

    # Setup channel encoder
    channels[c].setup()

    # Create and start channel thread
    threads[c] = threading.Thread()
    threads[c].name = c
    threads[c].run = channels[c].run
    threads[c].start()

    time.sleep(0.5)
    print()



def merge():
    """
    Merge muxes with TSDuck
    """

    print("Starting merge thread...\n\n")

    cmd = "tsp "
    for c in channels:
        port = 2000 + int(c)

        if c != "1":
            cmd += "-P merge \"tsp "
            cmd += f"-I ip 230.2.2.2:{port}\" "
        else:
            cmd += f"-I ip 230.2.2.2:{port} "
    
    cmd += "-O ip --enforce-burst 230.2.2.2:2000"

    tsduck = subprocess.call(
        cmd,
        shell=False,
        stdout=open(os.devnull, 'w'),
        stderr=subprocess.STDOUT
    )



def detect_deps():
    """
    Check for FFmpeg
    """

    if shutil.which("ffmpeg") is None:
        print("FFmpeg not found")
        exit(1)
    
    if shutil.which("tsp") is None:
        print("TSDuck not found")
        exit(1)


try:
    init()
except KeyboardInterrupt:
    stop_channels()
    print("\nExiting tsmgr...")
    exit(0)
