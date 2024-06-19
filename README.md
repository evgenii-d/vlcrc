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
from pathlib import Path
from vlcrc import VLCRemoteControl

# Initialize VLCRemoteControl
vlc = VLCRemoteControl('127.0.0.1', 50000)

# Play the current item
vlc.play()

# Add a file to the playlist
vlc.add(Path("/path/to/file.mp3"))

# Set the volume to 50
vlc.set_volume(50)

# Get the current playlist status
status = vlc.status()
print(status.data)
```

### Command-line

```txt
usage: vlcrc [-h] [-a ADDRESS] [-p PORT] [-t TIMEOUT] -c COMMAND

VLC Remote Control

options:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        Address of the VLC server [127.0.0.1]
  -p PORT, --port PORT  Port to use [50000]
  -t TIMEOUT, --timeout TIMEOUT
                        Socket connection timeout [0.1]
  -c COMMAND, --command COMMAND
                        The VLC Remote Control command to execute
```

## Remote control commands

```txt
add XYZ  . . . . . . . . . . . . add XYZ to playlist
enqueue XYZ  . . . . . . . . . queue XYZ to playlist
playlist . . . . .  show items currently in playlist
play . . . . . . . . . . . . . . . . . . play stream
stop . . . . . . . . . . . . . . . . . . stop stream
next . . . . . . . . . . . . . .  next playlist item
prev . . . . . . . . . . . .  previous playlist item
goto . . . . . . . . . . . . . .  goto item at index
repeat [on|off] . . . .  toggle playlist item repeat
loop [on|off] . . . . . . . . . toggle playlist loop
random [on|off] . . . . . . .  toggle random jumping
clear . . . . . . . . . . . . . . clear the playlist
status . . . . . . . . . . . current playlist status
title [X]  . . . . . . set/get title in current item
title_n  . . . . . . . .  next title in current item
title_p  . . . . . .  previous title in current item
chapter [X]  . . . . set/get chapter in current item
chapter_n  . . . . . .  next chapter in current item
chapter_p  . . . .  previous chapter in current item

seek X . . . seek in seconds, for instance `seek 12'
pause  . . . . . . . . . . . . . . . .  toggle pause
fastforward  . . . . . . . .  .  set to maximum rate
rewind  . . . . . . . . . . . .  set to minimum rate
faster . . . . . . . . . .  faster playing of stream
slower . . . . . . . . . .  slower playing of stream
normal . . . . . . . . . .  normal playing of stream
frame. . . . . . . . . .  play frame by frame
f [on|off] . . . . . . . . . . . . toggle fullscreen
info . . . . .  information about the current stream
stats  . . . . . . . .  show statistical information
get_time  . seconds elapsed since stream's beginning
is_playing . . . .  1 if a stream plays, 0 otherwise
get_title . . . . .  the title of the current stream
get_length . . . .  the length of the current stream

volume [X] . . . . . . . . . .  set/get audio volume
volup [X]  . . . . . . .  raise audio volume X steps
voldown [X]  . . . . . .  lower audio volume X steps
adev [device]  . . . . . . . .  set/get audio device
achan [X]. . . . . . . . . .  set/get audio channels
atrack [X] . . . . . . . . . . . set/get audio track
vtrack [X] . . . . . . . . . . . set/get video track
vratio [X]  . . . . . . . set/get video aspect ratio
vcrop [X]  . . . . . . . . . . .  set/get video crop
vzoom [X]  . . . . . . . . . . .  set/get video zoom
snapshot . . . . . . . . . . . . take video snapshot
strack [X] . . . . . . . . .  set/get subtitle track
key [hotkey name] . . . . . .  simulate hotkey press

help . . . . . . . . . . . . . . . this help message
logout . . . . . . .  exit (if in socket connection)
quit . . . . . . . . . . . . . . . . . . .  quit vlc
```

[1]:https://wiki.videolan.org/Documentation:Modules/rc
[2]:https://wiki.videolan.org/VLC_command-line_help
