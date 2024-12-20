# VLC Remote Control

A Python library for controlling VLC media player
via its [Remote Control interface][1].

## Features

- Control playback: play, pause, stop, next, previous.
- Playlist management: add, view, clear, repeat, loop, random.
- Volume control: get and set the volume.
- Audio device management: get and set the active audio device.
- Command Line Interface (CLI).

## Requirements

- Python 3.10+
- VLC media player with Remote Control (RC) interface enabled.

## Installation

### 0. Install VLC media player

Download the installer at <https://www.videolan.org/vlc/>

### 1. Ensure the RC Interface is Enabled

#### From the VLC UI

1. Open VLC and navigate to `Tools` -> `Preferences` -> `Show settings: All`.
2. Under `Interface` -> `Main Interfaces`, select `RC`.

#### From the Command Line (Optional, but Recommended)

| OS      | Command                                                  |
|---------|----------------------------------------------------------|
| Windows | `vlc --extraintf rc --rc-host=HOST:PORT`                 |
| Linux   | `vlc --extraintf oldrc --rc-fake-tty --rc-host=HOST:PORT`|

**Note:** Make sure the specified port (e.g., `PORT`) is open and accessible
in your firewall to allow remote control connections.

For more details, refer to the [VLC command-line help][2].

### 2. Import the library

```bash
pip install vlcrc
```

## Usage

### Python Library

```py
from pathlib import Path
from vlcrc import VLCRemoteControl

# Create a VLCRemoteControl instance
vlc = VLCRemoteControl('127.0.0.1', 50000)

# Add a file to the playlist
vlc.add(Path("/path/to/media/file.mp4"))

# Play media
vlc.play()

# Get the current playlist
playlist = vlc.playlist()
print(playlist)

# Get and set volume
current_volume = vlc.get_volume()
print(current_volume)
vlc.set_volume(100)

# Get audio devices and set an active one
devices = vlc.get_adev()
print(devices)
vlc.set_adev(devices[0].id)
```

#### Available Commands

| Command      | Description                                 |
|--------------|---------------------------------------------|
| `add`        | Add a file to the playlist.                 |
| `playlist`   | Get the current playlist.                   |
| `play`       | Play the current media.                     |
| `stop`       | Stop playback.                              |
| `next`       | Skip to the next media in the playlist.     |
| `prev`       | Skip to the previous media.                 |
| `goto`       | Go to a specific playlist index.            |
| `repeat`     | Toggle playlist item repeat.                |
| `loop`       | Toggle playlist loop.                       |
| `random`     | Toggle playlist random jumping.             |
| `clear`      | Clear the playlist.                         |
| `status`     | Get the current status of the player.       |
| `pause`      | Pause or resume playback.                   |
| `get_volume` | Get the current audio volume.               |
| `set_volume` | Set the audio volume (0-320).               |
| `get_adev`   | Get a list of available audio devices.      |
| `set_adev`   | Set the active audio device.                |
| `quit`       | Quit VLC.                                   |

### Command Line Interface (CLI)

```txt
usage: main.py [-h] host port {play,stop,next,prev,clear,status,pause,repeat,loop,random,playlist,quit,add,goto,volume,adev} ...

Command Line Interface for VLC Remote Control

positional arguments:
  host                  VLC host address (e.g., 127.0.0.1, 192.168.1.100)
  port                  VLC Remote Control interface port
  {play,stop,next,prev,clear,status,pause,repeat,loop,random,playlist,quit,add,goto,volume,adev}
                        Commands
    play                play command
    stop                stop command
    next                next command
    prev                prev command
    clear               clear command
    status              status command
    pause               pause command
    repeat              repeat command
    loop                loop command
    random              random command
    playlist            playlist command
    quit                quit command
    add                 Add file to playlist
    goto                Go to specific track
    volume              Get/set volume
    adev                Audio device control

options:
  -h, --help            show this help message and exit
```

[1]:https://wiki.videolan.org/Documentation:Modules/rc
[2]:https://wiki.videolan.org/VLC_command-line_help
