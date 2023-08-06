from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from pydantic import BaseModel, validator
from pydantic.dataclasses import dataclass
from typeguard import typechecked

from devinstaller_core import command as c
from devinstaller_core import exception as e
from devinstaller_core import utilities as u

ui = u.UserInteraction()


@dataclass
class ModuleInstallInstruction:
    """The class used to convert `init`, `command` and `config` into objects"""

    cmd: str
    rollback: Optional[str] = None


@dataclass
class ModuleBase(ABC):
    """The class which will be used by all the modules"""

    # pylint: disable=too-many-instance-attributes
    name: str
    alias: Optional[str] = None
    display: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    status: Optional[str] = None
    before: Optional[str] = None
    after: Optional[str] = None
    constants: Optional[Dict[str, str]] = None

    @validator("alias", pre=True, check_fields=False)
    @classmethod
    def alias_validator(cls, alias: Optional[str], values) -> str:
        """Set the alias if it is not provided."""
        if alias is None:
            return values["name"]
        return alias

    @validator("display", pre=True, check_fields=False)
    @classmethod
    def display_validator(cls, display: Optional[str], values) -> str:
        """Set the display if it is not provided."""
        if display is None:
            return values["name"]
        return display

    @validator("constants", pre=True, check_fields=False)
    @classmethod
    def convert_constant(
        cls, constants: Optional[List[Dict[str, str]]]
    ) -> Dict[str, str]:
        """Convert incomming dict into dict which can be used for
        constants replacing.
        """
        data: Dict[str, str] = {}
        if constants is None:
            return {}
        for i in constants:
            data[i["key"]] = i["value"]
        return data

    def __str__(self) -> str:
        if self.description is None:
            return f"{self.display}"
        return f"{self.display} - {self.description}"

    @abstractmethod
    def install(self) -> None:
        """Abstract install function for each module to be immplemented"""
        pass

    @abstractmethod
    def uninstall(self) -> None:
        """Abstract uninstall function for each module to be immplemented"""
        pass

    @typechecked
    def execute_instructions(
        self, instructions: List[ModuleInstallInstruction]
    ) -> None:
        """The function which handles installing of multi step commands.

        Args:
            steps: The list of steps which needs to be executed

        Raises:
            ModuleInstallationFailed
                if the installation of the module fails
            ModuleRollbackFailed
                if the rollback command fails
        """
        if instructions == []:
            return None
        for index, inst in enumerate(instructions):
            try:
                session = c.SessionSpec()
                session.run(inst.cmd)
            except e.CommandFailed:
                rollback_list = instructions[:index]
                rollback_list.reverse()
                try:
                    self.rollback_instructions(rollback_list)
                except e.ModuleRollbackFailed:
                    raise e.ModuleRollbackFailed
                raise e.ModuleInstallationFailed

    @classmethod
    @typechecked
    def rollback_instructions(
        cls, instructions: List[ModuleInstallInstruction]
    ) -> None:
        """Rollback the installation of a module

        Args:
            List of install instructions

        Raises:
            ModuleRollbackFailed
                if the rollback instructions fails
        """
        for inst in instructions:
            if inst.rollback is not None:
                try:
                    ui.print(f"Rolling back `{inst.cmd}` using `{inst.rollback}`")
                    session = c.SessionSpec()
                    session.run(inst.rollback)
                except e.CommandFailed:
                    raise e.ModuleRollbackFailed
