"""Group module
"""
from typing import List, Optional

from pydantic.dataclasses import dataclass

from devinstaller_core import module_base as mb


@dataclass
class ModuleGroup(mb.ModuleBase):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    optionals: Optional[List[str]] = None
    requires: Optional[List[str]] = None

    def install(self):
        pass

    def uninstall(self):
        pass
