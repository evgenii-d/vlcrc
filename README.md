# VLC Remote Control

A Python script to control VLC media player via its [Remote Control interface][1].

## Usage

### Enable VLC Remote Control interface

#### From the UI

1. Open VLC media player.
2. Go to Tools > Preferences (or press Ctrl+P).
3. At the bottom left, under "Show settings", select "All".
4. Navigate to Interface > Main interfaces.
5. Check the box next to Remote control interface.
6. Click Save.

#### From the command line (optional, but recommended)

|OS|Command|
|-|-|
|Windows|`vlc --extraintf rc --rc-host=HOST:PORT`|
|Linux|`vlc --extraintf oldrc --rc-fake-tty --rc-host=HOST:PORT`|

[VLC command-line help][2]

### Python module

```py
from vlcrc import VLCRemoteControl

# Initialize VLCRemoteControl
vlc = VLCRemoteControl('127.0.0.1', 50000)

# Play the current item
vlc.play()

# Add a file to the playlist
vlc.add('/path/to/file.mp3')

# Set the volume to 50
vlc.set_volume(50)

# Get the current playlist status
status = vlc.status()
print(status.data)
```

### Command-line

```txt
usage: vlcrc [-h] [--host HOST] [--port PORT] [--timeout TIMEOUT] --command COMMAND

VLC Remote Control

options:
  -h, --help         show this help message and exit
  --host HOST        Host [127.0.0.1]
  --port PORT        Port to use [50000]
  --timeout TIMEOUT  Socket connection timeout [0.1]
  --command COMMAND  VLC RC command
```

[1]:https://wiki.videolan.org/Documentation:Modules/rc
[2]:https://wiki.videolan.org/VLC_command-line_help
