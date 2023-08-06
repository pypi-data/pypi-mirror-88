"""Phony module
"""
import sys
from typing import List, Optional

from pydantic import validator
from pydantic.dataclasses import dataclass

from devinstaller_core import module_base as mb
from devinstaller_core import utilities

ui = utilities.ui


@dataclass
class ModulePhony(mb.ModuleBase):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    commands: Optional[List[mb.ModuleInstallInstruction]] = None

    @validator("commands")
    @classmethod
    def replace_var_in_install_inst(
        cls, install_inst: Optional[List[mb.ModuleInstallInstruction]], values
    ) -> Optional[List[mb.ModuleInstallInstruction]]:
        """The validator method which will replace all the variables in the
        `install_inst` with the `constants`
        """
        constants = values["constants"]
        if install_inst is None:
            return None
        for i in install_inst:
            i.cmd = i.cmd.format(**constants)
        return install_inst

    def install(self):
        """Install using the given commands
        """
        ui.print(f"Running commands in: {self.display}...")
        self.execute_instructions(self.commands)
        sys.exit(1)

    def uninstall(self):
        """Dummy method. Not part of the specification but here for initializing
        the object.
        """
