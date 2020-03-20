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
        opts = dict(config.items('source'))
        for o in opts:
            o += ":"
            print(f"   {o.title().ljust(14)}{opts[o[:-1]].upper()}")
        print()

        self.setup()


    def setup(self):
        """
        Setup channel
        """

        self.setup_source()


    def setup_source(self):
        """
        Setup channel source
        """

        src = self.config.get('source', 'type').upper()
        std = self.config.get('source', 'standard').upper()
        res = self.config.get('source', 'resolution').lower()
        fps = self.config.get('source', 'rate')

        if src == "TEST":
            self.source = self.src_test(res, fps)
        else:
            self.print(f"Unknown source \"{src}\"")
            return False
        
        self.print("Ready", "SOURCE")


    def src_test(self, res, fps):
        """
        Create test source (bars and tone)
        """

        opts = {
            "sd": [ "smptebars", "720x576" ],
            "hd": [ "smptehdbars", "1920x1080" ]
        }

        src = ffmpeg.input(
            f"{opts[res][0]}=size={opts[res][1]}:rate={str(fps)}",
            format="lavfi"
        )

        return src


    def print(self, msg="", src=""):
        """
        Print channel message to console
        """

        if src != "": src = f"[{src}]".upper()
        print(f"[{self.id}][\"{self.name}\"]{src}  {msg}")
