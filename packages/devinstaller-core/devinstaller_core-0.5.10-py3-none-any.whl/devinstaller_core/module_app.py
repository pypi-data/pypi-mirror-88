"""App module
"""
import sys
from typing import List, Optional, Union

from pydantic import validator
from pydantic.dataclasses import dataclass
from typeguard import typechecked

from devinstaller_core import command as c
from devinstaller_core import exception as e
from devinstaller_core import module_base as mb
from devinstaller_core import utilities as u

ui = u.UserInteraction()


@dataclass
class ModuleApp(mb.ModuleBase):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    version: Optional[str] = None
    executable: Optional[str] = None
    optionals: Optional[List[str]] = None
    requires: Optional[List[str]] = None
    install_inst: Optional[List[mb.ModuleInstallInstruction]] = None
    uninstall_inst: Optional[List[str]] = None
    bind: Optional[List[str]] = None

    @validator("install_inst")
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
            i.rollback = (
                i.rollback.format(**constants) if i.rollback is not None else None
            )
        return install_inst

    @validator("uninstall_inst")
    @classmethod
    def replace_var_in_uninstall_inst(
        cls, uninstall_inst: Optional[List[str]], values
    ) -> Optional[List[str]]:
        """The validator method which will replace all the variables in the
        `uninstall_inst` with the `constants`
        """
        constants = values["constants"]
        if uninstall_inst is None:
            return None
        for i in uninstall_inst:
            i = i.format(**constants)
        return uninstall_inst

    def install(self) -> None:
        """The function which installs app modules

        Args:
            module: The app module

        Returns:
            The response object of the module
        """
        ui.print(f"Installing module: {self.display}...")
        # installation_steps = create_instruction_list(self.install_inst)
        try:
            self.execute_instructions(self.install_inst)
            return None
        except e.ModuleRollbackFailed:
            ui.print(
                f"Rollback instructions for {self.display} failed. Quitting program."
            )
            sys.exit(1)

    def uninstall(self) -> None:
        """Uninstall the module using its rollback instructions.

        Args:
            module: The module which you want to uninstall
        """
        ui.print(f"Uninstalling module: {self.display}...")
        if self.uninstall_inst is None:
            ui.print(f"No un-installation instructions found for {self.display}.")
            return None
        try:
            for i in self.uninstall_inst:
                session = c.SessionSpec()
                session.run(i)
            return None
        except e.ModuleInstallationFailed:
            ui.print(f"Un-installation of {self.display} failed. Quitting program.")
            sys.exit(1)
