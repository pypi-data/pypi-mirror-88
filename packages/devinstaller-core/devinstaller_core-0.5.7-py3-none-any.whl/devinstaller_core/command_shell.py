import shlex
import subprocess

from devinstaller_core import exception as e
from devinstaller_core import extension as ex


class ExtSpec(ex.ExtSpec):
    LANGUAGE_CODE = "sh"
    LANGUAGE_NAME = "Shell"

    def run(self, command: str) -> None:
        """Runs the comand and returns None if no error else `subprocess.CalledProcessError` is raised

        Args:
            command: The path to the file

        Raises:
            CommandFailed
        """
        try:
            subprocess.run(shlex.split(command))
        except subprocess.CalledProcessError as err:
            raise e.CommandFailed(returncode=err.returncode, cmd=err.cmd)
