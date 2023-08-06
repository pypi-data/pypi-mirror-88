"""Phony module
"""
from typing import List, Optional

from pydantic.dataclasses import dataclass

from devinstaller_core import module_base as mb


@dataclass
class ModulePhony(mb.ModuleBase):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    commands: Optional[List[str]] = None

    def install(self):
        pass

    def uninstall(self):
        pass
