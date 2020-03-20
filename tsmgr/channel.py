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

        video, audio = self.setup_source()
        self.print_args(video)
        self.print_args(audio)

        output = self.setup_output(video, audio)
        self.print_args(output)
        output.overwrite_output().run()


    def setup_source(self):
        """
        Setup channel source
        """

        src = self.config.get('source', 'type').upper()
        res = self.config.get('source', 'resolution').lower()
        fps = self.config.get('source', 'rate')

        if src == "TEST":
            return self.src_test(res, fps)
        else:
            self.print(f"Unknown source \"{src}\"")
            return None, None


    def src_test(self, res, fps):
        """
        Create test source (bars and tone)
        """

        opts = {
            "sd": [ "smptebars", "720x576", 20 ],
            "hd": [ "smptehdbars", "1920x1080", 38 ]
        }

        bars = ffmpeg.input(
            f"{opts[res][0]}=size={opts[res][1]}:rate={str(fps)}",
            format="lavfi",
            re=None
        ).drawtext(
            x=20,
            y=20,
            text='%{localtime:%X}:%{eif:mod(n,' + fps + '):d:2}',
            font="Arial",
            fontsize=opts[res][2],
            fontcolor="white",
            box=1,
            boxcolor="black",
            boxborderw=opts[res][2]/4,
            escape_text=False
        )

        tone = ffmpeg.filter(
            (
                ffmpeg.input(f"sine=frequency=1000:sample_rate=48000", format="lavfi", re=None),
                ffmpeg.input(f"sine=frequency=1000:sample_rate=48000", format="lavfi", re=None)
            ),
            'join',
            inputs=2,
            channel_layout='stereo'
        ).filter(
            'volume',
            '0dB'
        )

        print("Ready", "SOURCE")
        return (bars, tone)


    def setup_output(self, video, audio):
        """
        Setup channel output
        """

        std = self.config.get('source', 'standard').upper()

        codec = {
            "MPEG-2": [ "mpeg2video", "mp2" ],
            "MPEG-4": [ "libx264", "aac" ]
        }

        return ffmpeg.output(
            video, audio,
            "bars-tone.mp4",
            vcodec=codec[std][0], acodec=codec[std][1]
        )


    def print_args(self, node):
        """
        Print compiled FFmpeg arguments
        """

        try:
            args = node.output("").compile()
        except AttributeError:
            args = node.compile()
        
        print(" ".join(args))


    def print(self, msg="", src=""):
        """
        Print channel message to console
        """

        if src != "": src = f"[{src}]".upper()
        print(f"[{self.id}][\"{self.name}\"]{src}  {msg}")
