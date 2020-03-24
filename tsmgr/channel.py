"""
channel.py
https://github.com/sam210723/tsmgr

MPEG transport stream manager for broadcast monitoring systems
"""

import ffmpeg
import os
import subprocess

class Channel:
    def __init__(self, chan_config, mgr_config):
        self.chan_config = chan_config
        self.id = self.chan_config.get('channel', 'id')
        self.name = self.chan_config.get('channel', 'name')
        self.provider = self.chan_config.get('channel', 'provider')
        self.muxrate = self.chan_config.get('channel', 'muxrate')
        self.quiet = self.chan_config.getboolean('channel', 'quiet')

        self.mgr_config = mgr_config
        self.table_ver = self.mgr_config.get('tsmgr', 'table_version')

        # Print channel configuration to console
        self.print_config()


    def setup(self):
        """
        Setup channel encoder
        """

        # Setup audio and video sources
        self.video, self.audio = self.setup_source()

        # Setup channel output multiplex
        self.output = self.setup_output(self.video, self.audio)


    def setup_source(self):
        """
        Setup channel source
        """

        config = dict(self.chan_config.items('source'))

        if config['type'] == "test":
            return self.src_test(config)
        elif config['type'] == "dshow":
            return self.src_dshow(config)
        else:
            self.print(f"Unknown source \"{config['type']}\"")
            return None, None


    def setup_output(self, video, audio):
        """
        Setup channel output
        http://www.waveguide.se/?article=creating-dvb-t-compatible-mpeg2-streams-using-ffmpeg
        """

        std = self.chan_config.get('source', 'standard').upper()

        codec = {
            "MPEG-2": [ "mpeg2video", "mp2" ],
            "MPEG-4": [ "libx264", "aac" ]
        }

        # Output port based on channel number
        port = 2000 + int(self.chan_config.get('channel', 'id'))

        # Check for missing audio stream
        streams = (video,) if audio == None else (video, audio)

        return ffmpeg.output(
            *streams,
            f"udp://230.2.2.2:{port}?pkt_size=1316",
            format="mpegts",
            muxrate=self.muxrate,
            mpegts_transport_stream_id=self.chan_config.get('channel', 'id'),
            mpegts_original_network_id=0x1337,
            mpegts_service_id=self.chan_config.get('channel', 'id'),
            mpegts_service_type="digital_tv",
            mpegts_pmt_start_pid=0x0020 + int(self.id),
            mpegts_start_pid=0x0100 + (0x0010 * int(self.id)) + 1,
            mpegts_flags="system_b",
            tables_version=self.table_ver,
            **{
                'metadata': f'service_name={self.name}',
                'metadata:': f'service_provider={self.provider}'
            },
            vcodec=codec[std][0],
            acodec=codec[std][1]
        )


    def run(self):
        """
        Run channel encoder
        """

        self.process = (
            self.output.run_async(
                quiet=self.quiet
                # Fix applied to _run.py from https://github.com/kkroening/ffmpeg-python/issues/195
            )
        )
        self.print("Running")

        return_code = self.process.wait()
        if return_code:
            self.print(f"Exited with code {return_code}")


    def stop(self):
        """
        Stop encoder thread
        """

        self.print("Stopping")
        self.process.kill()


    def src_dshow(self, config):
        """
        Create DirectShow source
        http://ffmpeg.org/ffmpeg-devices.html#dshow
        https://trac.ffmpeg.org/wiki/DirectShow
        """

        # Combine generic and source-specific options
        config.update(dict(self.chan_config.items('dshow')))

        # Resolution presets
        presets = {
            "SD": "720x576",
            "HD": "1920x1080"
        }

        dshow = ffmpeg.input(
            f"video={config['video']}:audio={config['audio']}",
            format="dshow",
            s=presets[config['resolution']],
            framerate=config['fps'],
            pixel_format=config['format'],
            #show_video_device_dialog="true",
            re=None,
            rtbufsize="500M"
        )

        self.print("Ready")
        return dshow, None


    def src_test(self, config):
        """
        Create test source (bars and tone)
        """

        # Combine generic and source-specific options
        config.update(dict(self.chan_config.items('test')))

        # Resolution presets
        presets = {
            "SD": [ "smptebars",   "720x576",   20 ],
            "HD": [ "smptehdbars", "1920x1080", 38 ]
        }

        # Generate SMPTE bars
        bars = ffmpeg.input(
            self.lavfi(
                presets[config['resolution']][0],
                size=presets[config['resolution']][1],
                rate=config['fps']
            ),
            format="lavfi",
            re=None
        )

        # Generate timecode text
        if self.chan_config.getboolean('test', 'timecode'):
            bars = bars.drawtext(
                x=20,
                y=20,
                text='%{localtime:%X}:%{eif:mod(n,' + config['fps'] + '):d:2}',
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
        
        # Text overlay
        if config['text']:
            path = os.path.abspath("tsmgr\\channels\\" + config['text'])
            bars = bars.drawtext(
                x="(w-text_w)/2",
                y="(h-text_h)/2",
                textfile=path,
                reload=1,
                fontfile="C:\\Windows\\Fonts\\Arialbd.ttf",
                fontsize=presets[config['resolution']][2],
                fontcolor="white",
                line_spacing=15,
                box=1,
                boxcolor="black",
                boxborderw=presets[config['resolution']][2]/1.5,
                escape_text=False
            )

        if config['banner']:
            bars = bars.drawtext(
                x="(w-text_w)/2",
                y=60,
                text=config['banner'],
                fontfile="C:\\Windows\\Fonts\\Arialbd.ttf",
                fontsize=presets[config['resolution']][2],
                fontcolor="white",
                box=1,
                boxcolor="black",
                boxborderw=presets[config['resolution']][2]/3,
                escape_text=False
            )

        # Generate sine tone
        if self.chan_config.getboolean('test', 'tone'):
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

        self.print("Ready")
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
        options = dict(self.chan_config.items('source'))
        options.update({"muxrate": f"{int(self.muxrate)/1e6} Mbps"})
        for o in options:
            option = (o + ":").ljust(14).upper()
            value = options[o]
            print(f"   {option}{value}")


    def print(self, msg="", src=""):
        """
        Print channel message to console
        """

        if src != "": src = f"[{src}]".upper()
        pre = f"[{self.id}][\"{self.name}\"]{src}"
        print(f"{pre.ljust(25)}{msg}")
