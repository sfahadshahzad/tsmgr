"""
channel.py
https://github.com/sam210723/tsmgr

MPEG transport stream manager for broadcast monitoring systems
"""

import ffmpeg
import os

class Channel:
    def __init__(self, config):
        self.config = config
        self.name = config.get('channel', 'name')
        self.id = config.get('channel', 'id')

        # Print channel configuration to console
        self.print_config()

        # Setup audio and video sources
        self.video, self.audio = self.setup_source()

        # Setup channel output multiplex
        self.output = self.setup_output(self.video, self.audio)

        self.output.overwrite_output().run()    #TODO


    def setup_source(self):
        """
        Setup channel source
        """

        config = dict(self.config.items('source'))

        if config['type'] == "test":
            return self.src_test(config)
        else:
            self.print(f"Unknown source \"{config['type']}\"")
            return None, None


    def setup_output(self, video, audio):
        """
        Setup channel output
        """

        std = self.config.get('source', 'standard').upper()

        codec = {
            "MPEG-2": [ "mpeg2video", "mp2" ],
            "MPEG-4": [ "libx264", "aac" ]
        }

        # Output port based on channel number
        port = 2000 + int(self.config.get('channel', 'id'))

        # Check for missing audio stream
        streams = (video,) if audio == None else (video, audio)

        return ffmpeg.output(
            *streams,
            f"udp://230.2.2.2:{port}?pkt_size=1316",
            format="mpegts",
            muxrate=512000,
            metadata=f"service_name={self.config.get('channel', 'name')}",
            mpegts_service_id=self.config.get('channel', 'id'),
            #streamid="0:0x0101",            # Video PID
            #mpegts_start_pid=0x0012,        # PCR PID
            #mpegts_pmt_start_pid=0x0100,    # PMT PID
            vcodec=codec[std][0],
            acodec=codec[std][1]
        )



    def src_test(self, config):
        """
        Create test source (bars and tone)
        """

        # Combine generic and source-specific options
        config.update(dict(self.config.items('test')))

        # Resolution presets
        presets = {
            "sd": [ "smptebars",   "720x576",   20 ],
            "hd": [ "smptehdbars", "1920x1080", 38 ]
        }

        # Generate SMPTE bars
        bars = ffmpeg.input(
            self.lavfi(
                presets[config['resolution']][0],
                size=presets[config['resolution']][1],
                rate=config['rate']
            ),
            format="lavfi",
            re=None
        )

        # Generate timecode text
        if self.config.getboolean('test', 'timecode'):
            bars = bars.drawtext(
                x=20,
                y=20,
                text='%{localtime:%X}:%{eif:mod(n,' + config['rate'] + '):d:2}',
                font="Arial",
                fontsize=presets[config['resolution']][2],
                fontcolor="white",
                box=1,
                boxcolor="black",
                boxborderw=presets[config['resolution']][2]/4,
                escape_text=False
            )
        
        # Image overlay
        if config['image']:
            path = os.path.abspath("tsmgr\\channels\\" + config['image'])
            image = ffmpeg.input(path)
            bars = bars.overlay(
                image,
                x="(main_w-overlay_w)/2",
                y="(main_h-overlay_h)/2"
            )

        # Generate sine tone
        if self.config.getboolean('test', 'tone'):
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
                '-6dB'
            )
        else:
            tone = None

        print("Ready", "SOURCE")
        return (bars, tone)


    def lavfi(self, graph, **kwargs):
        """
        Create lavfi source string
        """

        s = f"{graph}="
        for key, value in kwargs.items():
            s += f"{key}={value}:"

        return s

    def print_args(self, node):
        """
        Print compiled FFmpeg arguments
        """

        try:
            args = node.output("").compile()
        except AttributeError:
            args = node.compile()
        
        print(" ".join(args))

    def print_config(self):
        """
        Print channel configuration
        """

        self.print()
        options = dict(self.config.items('source'))
        for o in options:
            option = (o.title() + ":").ljust(14)
            value = options[o].upper()
            print(f"   {option}{value}")
        print()

    def print(self, msg="", src=""):
        """
        Print channel message to console
        """

        if src != "": src = f"[{src}]".upper()
        print(f"[{self.id}][\"{self.name}\"]{src}  {msg}")
