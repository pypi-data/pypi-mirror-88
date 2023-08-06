"""Link module
"""
from typing import List, Optional

from pydantic.dataclasses import dataclass

from devinstaller_core import module_base as mb


@dataclass
class ModuleLink(mb.ModuleBase):
    """The class which will be used by all the modules
    """

    # pylint: disable=too-many-instance-attributes
    init: Optional[List[mb.ModuleInstallInstruction]] = None
    config: Optional[List[mb.ModuleInstallInstruction]] = None
    optionals: Optional[List[str]] = None
    owner: Optional[str] = None
    requires: Optional[List[str]] = None
    source: Optional[str] = None
    symbolic: Optional[bool] = None
    target: Optional[str] = None
    create: bool = True
    rollback: bool = True

    def install(self):
        pass

    def uninstall(self):
        pass
