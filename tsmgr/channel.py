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
        src = src.lower()
        self.print(f"Starting \"{src.upper()}\" source")

        if src == "test":
            ffmpeg.input(
                self.test_src(
                    self.config.get(
                        'input',
                        'resolution'
                    ).lower(),
                    25
                ),
                format="lavfi"
        else:
            self.print(f"Unknown source \"{src}\"")


    def test_src(self, res, fps):
        """
        Generate LAVFI test source string
        """

        if res == "sd": res == ""
        pix = {
            "sd": "720x576",
            "hd": "1920x1080"
        }
        
        return f"smpte{res}bars=size={pix[res]}:rate={str(fps)}"


    def print(self, msg=""):
        """
        Print channel message to console
        """

        print(f"[{self.id}][\"{self.name}\"]  {msg}")
