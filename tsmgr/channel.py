"""
channel.py
https://github.com/sam210723/tsmgr

MPEG transport stream manager for broadcast monitoring systems
"""

import ffmpeg

class Channel:
    def __init__(self, config):
        self.config = config
        self.name = config.get('channel', 'name')
        self.id = config.get('channel', 'id')

        self.print()

        # Print input options
        opts = dict(config.items('input'))
        for o in opts:
            print(f"   {o.title()}:   {opts[o].upper()}")
        print()

        self.setup()


    def setup(self):
        """
        Setup channel
        """

        src = self.config.get('input', 'source')
        self.setup_source(src)


    def setup_source(self, src):
        """
        Setup channel source
        """

        if src.lower() == "test":
            self.print(f"Starting TEST source")
        else:
            self.print(f"Unknown source \"{src}\"")


    def print(self, msg=""):
        """
        Print channel message to console
        """

        print(f"[{self.id}][\"{self.name}\"]  {msg}")
