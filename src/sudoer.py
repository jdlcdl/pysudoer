"""sudoer.py"""

import re
import io
import sys
import tempfile
import subprocess
import hashlib
import typing

from .sudoer_options import SudoerOptions

EXEC_OPTIONS = { "env": None }


class Sudoer:
    """
    Run a subprocess with administrative privileges,
    prompting the user with a graphical OS dialog if necessary.
    Useful for background subprocesse which run native kivy apps that need sudo.

    * Windows, uses elevate utility with native User Account Control
      (UAC) prompt (no PowerShell required)
    
    * OS X, uses bundled applet (inspired by Joran Dirk Greef)
    
    * Linux, uses system pkexec or gksudo (system or bundled).

    Refactored from https://www.npmjs.com/package/@o/electron-sudo
    """
    
    def __init__(
        self,
        name: str,
        child_process: subprocess.Popen,
        icns: str = None
    ):
        self.options = SudoerOptions(name=name, icns=icns)
        self.platform = sys.platform
        self.tmp_dir = tempfile.mkdtemp()

    @property
    def options(self) -> SudoerOptions:
        """Getter for options"""
        return self._options

    @options.setter
    def options(self, value: str):
        """Setter for options"""
        self._options = value

    @property
    def child_process(self) -> subprocess.Popen:
        """Getter for child_process"""
        return self._child_process

    @child_process.setter
    def child_process(self, value: str):
        """Setter for child_process"""
        self._child_process = value
    
    @property
    def platform(self) -> str:
        """Getter for platform"""
        return self._platform

    @platform.setter
    def platform(self, value: str):
        """Setter for platform"""
        self._platform = value

    @property
    def temp_dir(self) -> str:
        """Getter for temp_dir"""
        return self._temp_dir

    @temp_dir.setter
    def temp_dir(self, value: str):
        """Setter for temp_dir"""
        self._temp_dir = value

    def hash(self, buffer: io.BytesIO = io.BytesIO(b"")):
        """Create a hash for Sudoer object"""
        h = hashlib.new('sha256')
        for s in ["kivy-sudo", self.options.name, buffer.getvalue().hex()]:
            h.update(s.encode())
        return h.hexdigest()[:-32]

    @staticmethod
    def join_env(options: typing.Dict[str, str] = {}):
        """Return an array of `key=value` strings for a given dictionary"""
        return [ f"{key}={val}" for key,val in options.items() ]

    @staticmethod
    def escape_double_quotes(message: str = ""):
        """Escape a message with double quotes"""
        return message.replace('"', '\\"')

    @staticmethod
    def enclose_double_quotes(message: str = ""):
        """Enclose a message without double quotes"""
        return message.replace(message, f"\"{message}\"")

    @staticmethod
    def kill(pid: int):
        """kill a process """
        if not pid:
            pass
        else:
            pass