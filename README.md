# 📺 tsmgr - Transport Stream Manager

[![GitHub license](https://img.shields.io/github/license/sam210723/tsmgr.svg)](https://github.com/sam210723/tsmgr/blob/master/LICENSE)

**tsmgr** is a tool for creating custom [MPEG-TS](https://en.wikipedia.org/wiki/MPEG_transport_stream) multiplexes in real-time as part of an IP-based broadcast monitoring system.

It relies heavily on [FFmpeg](https://www.ffmpeg.org/) and [GStreamer](https://gstreamer.freedesktop.org/) for stream encoding, and [TSDuck](https://tsduck.io/) for stream routing.


# Installing
## Windows 10
 - FFmpeg
 - Python 3.8
 - PIP
 - ffmpeg-python
 - TSDuck
 - GStreamer

## Ubuntu 18.04
```
sudo apt-get update
sudo apt-get install python3.8 python3-pip ffmpeg

wget https://github.com/tsduck/tsduck/releases/download/v3.20-1689/tsduck_3.20-1689_amd64.deb

sudo apt-get install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc \
gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 \
gstreamer1.0-qt5 gstreamer1.0-pulseaudio

git clone https://github.com/sam210723/tsmgr
cd tsmgr
pip install -r requirements.txt
```
