from typing import List, Optional

from pydantic.dataclasses import dataclass
from typeguard import typechecked

from devinstaller_core import common_models as c
from devinstaller_core import exception as e
from devinstaller_core import utilities as u


@dataclass
class Module:
    """The class for interface modules"""

    name: str
    before: Optional[str] = None
    after: Optional[str] = None


@dataclass
class BlockInterface:
    """The class for interface"""

    # pylint: disable=too-many-instance-attributes
    name: str
    description: Optional[str] = None
    before: Optional[str] = None
    after: Optional[str] = None
    before_each: Optional[str] = None
    after_each: Optional[str] = None
    modules: Optional[List[Module]] = None

    def __str__(self) -> str:
        if self.description is None:
            return f"{self.name}"
        return f"{self.name} - {self.description}"


@typechecked
def get_interface(
    interface_list: List[c.TypeInterface], interface_name: Optional[str] = None
) -> BlockInterface:
    if interface_name is None:
        interface_name = select_interface(interface_list=interface_list)
    interface_result: List[c.TypeInterface] = []
    for item in interface_list:
        if item["name"] == interface_name:
            interface_result.append(item)
    if len(interface_result) < 1:
        raise e.SpecificationError(
            error=interface_name,
            error_code="S100",
            message="The interface name you have given doesn't match with any interface in the spec file.",
        )
    if len(interface_result) > 1:
        raise e.SpecificationError(
            error=interface_name,
            error_code="S100",
            message="Your spec file has more than one interface with the same name. You need to do something about this.",
        )
    # TODO Check the `modules` key in InterfaceBlock
    obj = interface_result[0]
    return BlockInterface(**obj)


def select_interface(interface_list: List[c.TypeInterface]) -> str:
    """Ask user to select one interface"""
    title = "Can you select one interface for me?"
    choices = [i["name"] for i in interface_list]
    ui = u.UserInteraction()
    selection = ui.select(title, choices)
    return selection
