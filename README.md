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

# Formats
| Standard | Video | Audio |
| -------- | ----- | ----- |
| ``MPEG-2`` | [H.262](https://en.wikipedia.org/wiki/H.262/MPEG-2_Part_2)  (MPEG-2 Part 2)         | [MPEG-1 Layer II](https://en.wikipedia.org/wiki/MPEG-1_Audio_Layer_II) (MP2) |
| ``MPEG-4`` | [H.264](https://en.wikipedia.org/wiki/Advanced_Video_Coding) (AVC / MPEG-4 Part 10) | [AAC](https://en.wikipedia.org/wiki/Advanced_Audio_Coding) (ADTS)            |

# PID Mapping
| Channel | PMT        | Video      | Audio      | TS ID |
| ------- | ---------- | ---------- | ---------- | ----- |
| 1       | ``0x0021`` | ``0x0111`` | ``0x0112`` | 1     |
| 2       | ``0x0022`` | ``0x0121`` | ``0x0122`` | 2     |
| 3       | ``0x0023`` | ``0x0131`` | ``0x0132`` | 3     |

# Configuration
## ``channel``
| Key          | Description |
| ------------ | ----------- |
| ``id``       | Channel Number (used in TS PIDs/ID and UDP Port) |
| ``name``     | Channel Name |
| ``provider`` | Program Provider |
| ``muxrate``  | Multiplex Bitrate |

## ``source``
| Key            | Description |
| -------------- | ----------- |
| ``type``       | Source Type (``test``, ``dshow``) |
| ``standard``   | MPEG Standard (``MPEG-2``, ``MPEG-4``) |
| ``resolution`` | Video Resolution (SD: ``720x576``, HD: ``1920x1080``) |
| ``rate``       | Frame Rate |

## ``test``
| Key          | Description |
| ------------ | ----------- |
| ``tone``     | 1 kHz Sine Tone (``yes``/``no``) |
| ``timecode`` | Timecode Overlay (``yes``/``no``) |
| ``image``    | Image Overlay (file path) |
| ``text``     | Text Overlay (file path) |
| ``banner``   | Banner Text (string) |

## ``dshow``
| Key        | Description |
| ---------- | ----------- |
| ``video``  | Video Device Name |
| ``audio``  | Audio Device Name |
| ``format`` | Video Format (yuyv422) |
