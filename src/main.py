""" VLC Remote Control """

import re
import sys
import socket
import argparse
from pathlib import Path
from dataclasses import dataclass


class ArgsNamespace(argparse.Namespace):
    """ A class to represent parsed command-line arguments """
    # pylint: disable=too-few-public-methods
    host: str
    port: int
    timeout: float
    command: str


class VLCRemoteControl:
    """ Control VLC media player via Remote Control interface """

    def __init__(self, host: str, port: int, timeout: float = 0.1) -> None:
        """ Initialize VLCRemoteControl

        Args:
            host (str): Hostname or IP address of the VLC instance
            port (int): Port number of the VLC RC interface
            timeout (float, optional): 
                Socket connection timeout in seconds. Defaults to 0.1.
        """
        self.host = host
        self.port = port
        self.timeout = timeout

    @dataclass
    class AudioDevice:
        """ System audio device """
        id: str
        name: str

    @dataclass
    class Respond:
        """ VLC Remote Control interface respond """
        success: bool
        data: list[str]

    def _filter_respond(self, data: list[str]) -> list[str]:
        """ Split data by "\r\n", remove empty and duplicates. 
            Order preserved.
        """
        result = []
        for item in data:
            result.extend(list(filter(None, item.split("\r\n"))))
        return list(dict.fromkeys(result))

    def _send(self, command: str) -> Respond:
        """ Send a command to VLC and receive the response

        Args:
            command (str): The VLC RC command to send

        Returns:
            Respond: 
                A Respond object containing 
                the success status and response data
        """
        respond_data: list[str] = []
        address = (self.host, self.port)
        try:
            with socket.create_connection(address, self.timeout) as rc_socket:
                rc_socket.sendall(str(command).encode() + b"\n")
                rc_socket.shutdown(1)
                while True:
                    respond = rc_socket.recv(4096).decode()
                    if not respond:
                        break
                    respond_data.append(respond)
        except (TimeoutError, ConnectionRefusedError, socket.error) as error:
            data = [f"VLC Remote Control is unavailable: {error}"]
            return VLCRemoteControl.Respond(False, data)

        for record in respond_data:
            if "unknown command" in record.lower():
                data = [f"Unknown command `{command.split()[0]}`"]
                return VLCRemoteControl.Respond(False, data)

        result = self._filter_respond(respond_data)
        return VLCRemoteControl.Respond(True, result)

    def exec(self, command: str) -> Respond:
        """ Execute given command 'as is' """
        return self._send(command)

    def add(self, file: Path) -> bool:
        """ Add a file to the playlist

        Args:
            file (Path): Path object representing the file to add

        Raises:
            FileNotFoundError: 
                If the specified file does not exist or is a directory

        Returns:
            bool: True if the command was successful, False otherwise
        """
        if not file.exists() or file.is_dir():
            raise FileNotFoundError
        respond = self._send(f"add {file.as_posix()}")
        return respond.success

    def play(self) -> bool:
        """ Play the current stream """
        respond = self._send("play")
        return respond.success

    def stop(self) -> bool:
        """ Stop the current stream """
        respond = self._send("stop")
        return respond.success

    def next(self) -> bool:
        """ Go to the next item in the playlist """
        respond = self._send("next")
        return respond.success

    def prev(self) -> bool:
        """ Go to the previous item in the playlist """
        respond = self._send("prev")
        return respond.success

    def goto(self, index: int) -> bool:
        """ Go to the specified playlist index

        Args:
            index (int): The index to go to (starting from 1)

        Raises:
            ValueError: If the index is less than or equal to 0

        Returns:
            bool: True if the command was successful, False otherwise
        """
        if index <= 0:
            raise ValueError("Index must be greater than zero")
        respond = self._send(f"goto {index}")
        return respond.success

    def clear(self) -> bool:
        """ Clear the playlist """
        respond = self._send("clear")
        return respond.success

    def status(self) -> Respond:
        """ Get the current playlist status """
        respond = self._send("status")
        return respond

    def pause(self) -> bool:
        """ Toggle pause/play """
        respond = self._send("pause")
        return respond.success

    def get_volume(self) -> int:
        """Get the current audio volume

        Returns:
            int: 
                The current audio volume (0-320), 
                or -1 if the volume could not be retrieved
        """
        respond = self._send("volume")
        for item in respond.data:
            match = re.search(r"audio volume:\s*(\d+)", item)
            if match:
                return int(match.group(1))
        return -1

    def set_volume(self, value: int) -> bool:
        """ Set the audio volume

        Args:
            value (int): Volume level (0-320)

        Raises:
            ValueError: If the volume is outside the range of 0-320

        Returns:
            bool: True if the command was successful, False otherwise
        """
        if not 0 <= value <= 320:
            raise ValueError("Value must be between 0 and 320")
        respond = self._send(f"volume {value}")
        return respond.success

    def get_adev(self) -> list[AudioDevice]:
        """ Get a list of available audio devices """
        devices: list[VLCRemoteControl.AudioDevice] = []
        respond = self._send("adev")
        for item in respond.data:
            if item[:2] == "| ":
                tmp = item[2:].split(" - ", 1)
                device = VLCRemoteControl.AudioDevice(tmp[0], tmp[1])
                if device.id:
                    devices.append(device)
        return devices

    def set_adev(self, device_id: str) -> bool:
        """ Set the active audio device """
        respond = self._send(f"adev {device_id}")
        return respond.success

    def quit(self) -> bool:
        """ Quit VLC """
        respond = self._send("quit")
        return respond.success


def parse_arguments() -> ArgsNamespace:
    """ Parse command-line arguments """
    parser = argparse.ArgumentParser(
        prog="vlcrc", description="VLC Remote Control",
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("--host", type=str, default="127.0.0.1",
                        help="Host [127.0.0.1]")
    parser.add_argument("--port", type=int, default=50000,
                        help="Port to use [50000]")
    parser.add_argument("--timeout", type=float, default=0.1,
                        help="Socket connection timeout [0.1]")
    parser.add_argument("--command", type=str, required=True,
                        help="VLC RC command")

    return parser.parse_args(namespace=ArgsNamespace())


if __name__ == "__main__":
    args = parse_arguments()
    vlc_rc = VLCRemoteControl(args.host, args.port, args.timeout)
    vlc_respond = vlc_rc.exec(args.command.lower())
    sys.stdout.write("\n".join(vlc_respond.data))
