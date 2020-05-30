"""NAPALM driver for Ubiquiti AirOS Using SSH"""

from __future__ import unicode_literals

import re
import socket

# Import NAPALM base
from napalm.base import NetworkDriver

# Import NAPALM exceptions
from napalm.base.exceptions import (
    ConnectionClosedException,
)



class AirOSDriver(NetworkDriver):

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Constructor.
        :param hostname:
        :param username:
        :param password:
        :param timeout:
        :param optional_args:
        """
        self.device = None
        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout

        if optional_args is None:
            optional_args = {}

        # Netmiko possible arguments
        self._netmiko_optional_args = {
            'port': None,
            'verbose': False,
            'global_delay_factor': 1,
            'use_keys': False,
            'key_file': None,
            'ssh_strict': False,
            'system_host_keys': False,
            'alt_host_keys': False,
            'alt_key_file': '',
            'ssh_config_file': None,
            'allow_agent': False,
            'keepalive': 30
        }

        # Build dict of any optional Netmiko args
        self._netmiko_optional_args.update(optional_args)

    def open(self):
        """Open a connection to the device.
        """
        device_type = "linux"

        self.device = self._netmiko_open(
            device_type, netmiko_optional_args=self._netmiko_optional_args
        )

    def close(self):
        """Close the connection to the device and do the necessary cleanup."""

        self._netmiko_close()

    def is_alive(self):
        """return: a flag with the state of the connection."""
        null = chr(0)
        if self.device is None:
            return {'is_alive': False}

        try:
            # Try sending ASCII null byte to maintain the connection alive
            self.device.write_channel(null)
            return {'is_alive': self.device.remote_conn.transport.is_active()}
        except (socket.error, EOFError):
            # If unable to send, we can tell for sure that the connection
            # is unusable
            return {'is_alive': False}


    def _send_command(self, command):
        """Wrapper for self.device.send.command().
        If command is a list will iterate through commands until valid command.
        """
        try:
            if isinstance(command, list):
                for cmd in command:
                    output = self.device.send_command(cmd)
                    if ": not found" not in output:
                        break
            else:
                output = self.device.send_command(command)
            return output
        except (socket.error, EOFError) as e:
            raise ConnectionClosedException(str(e))

    def cli(self, commands):
        """Execute a list of commands and return the output in a dictionary format using the command
        Example input:
        ['dis version', 'dis cu']
        """

        cli_output = dict()
        if type(commands) is not list:
            raise TypeError("Please enter a valid list of commands!")

        for command in commands:
            output = self.device.send_command(command)
            cli_output.setdefault(command, {})
            cli_output[command] = output

        return cli_output

    def get_config(self, retrieve="all", full=False, sanitized=False):
        """
        Get config from device.
        Returns the running configuration as dictionary.
        The candidate and startup are always empty string for now
        """

        configs = {"startup": "", "running": "", "candidate": ""}

        if retrieve in ("startup", "all"):
            command = "cat /tmp/system.cfg"
            output = self._send_command(command)
            configs["startup"] = output.strip()

        if retrieve in ("running", "all"):
            command = "cat /tmp/running.cfg"
            output = self._send_command(command)
            configs["running"] = output.strip()


        return configs

