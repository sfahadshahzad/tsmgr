# 📺 tsmgr - Transport Stream Manager

[![GitHub license](https://img.shields.io/github/license/sam210723/tsmgr.svg)](https://github.com/sam210723/tsmgr/blob/master/LICENSE)

**tsmgr** is a tool for creating custom [MPEG-TS](https://en.wikipedia.org/wiki/MPEG_transport_stream) multiplexes in real-time as part of an IP-based broadcast monitoring system.

It relies heavily on [FFmpeg](https://www.ffmpeg.org/) and [GStreamer](https://gstreamer.freedesktop.org/) for stream encoding, and [TSDuck](https://tsduck.io/) for stream routing.


# Installing
## Windows 10
 - [FFmpeg](https://ffmpeg.zeranoe.com/builds/)
 - Python >3.6
 - PIP
 - ffmpeg-python
 - TSDuck
 - GStreamer

## Ubuntu 18.04
```
sudo apt-get update
sudo apt-get install python3.6 python3-pip ffmpeg

wget https://github.com/tsduck/tsduck/releases/download/v3.20-1689/tsduck_3.20-1689_amd64.deb

sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc \
gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 \
gstreamer1.0-qt5 gstreamer1.0-pulseaudio

git clone https://github.com/sam210723/tsmgr
cd tsmgr
pip install -r requirements.txt
```

# Network
All source encoders use multicast address ``230.2.2.2`` and a port number based on the channel ID of the encoder (``2000 + channel_id``). The master multiplex uses port ``2000``.

# PID Mapping
| Channel | PMT        | Video      | Audio      | TS ID |
| ------- | ---------- | ---------- | ---------- | ----- |
| 1       | ``0x0100`` | ``0x0101`` | ``0x0102`` | 1     |
| 2       | ``0x0200`` | ``0x0201`` | ``0x0202`` | 2     |
| 3       | ``0x0300`` | ``0x0301`` | ``0x0302`` | 3     |
