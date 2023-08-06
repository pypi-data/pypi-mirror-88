from typing import Any, Dict, List

from typeguard import typechecked

from devinstaller_core import constants as c
from devinstaller_core import extension as ex


class UserInteraction(ex.BaseExtension[ex.ExtUserInteraction]):
    """Create a session for executing prog files"""

    def __init__(self) -> None:
        ext_class = c.UserInteraction.EXTENSION_CLASS
        builtin_extensions = c.UserInteraction.BUILTIN_EXTENSIONS
        super().__init__(builtin_extensions=builtin_extensions, ext_class=ext_class)
        abs_methods = getattr(ex.ExtUserInteraction, "__abstractmethods__")
        for method in list(abs_methods):
            setattr(self, method, getattr(self.return_object, method))

    def select(self, title: str, choices: List[str]) -> str:
        """Ask user to select one of the choices"""

    def print(self, message: Any) -> None:
        """Prints the given object into console using rich-text"""

    def checkbox(self, title: str, choices: List[str]) -> List[str]:
        """Ask user to select one or more choices"""

    def confirm(self, title: str) -> bool:
        """Ask user to confirm a decision"""

    def load_extension(self, extension: ex.ExtUserInteraction):
        """Loading extension"""
        self.return_object = extension


ui = UserInteraction()


class Dictionary:
    @classmethod
    @typechecked
    def remove_key(cls, input_dictionary: Dict[Any, Any], key: str) -> Dict[Any, Any]:
        """Remove the key and its value from the dictionary

        The original dictionary is not modified instead a copy is made
        and modified and that is returned.

        Args:
            input_dictionary: Any dictionary
            key: The key and its value you want to remove

        Returns:
            A new dictionary without the specified key
        """
        if key not in input_dictionary:
            return input_dictionary
        new_dictionary = input_dictionary.copy()
        new_dictionary.pop(key)
        return new_dictionary


class Compare:
    """All the methods you need to compare stuffs."""

    @classmethod
    @typechecked
    def strings(cls, *args: str) -> bool:
        """Compare all the strings with each other (case insensitive)

        Takes in any number of string arguments.
        At least one argument required else it will return False.
        If one argument then it will return True.

        Returns:
            True if all matches else False
        """
        if len({v.casefold() for v in args}) != 1:
            return False
        return True

    @classmethod
    @typechecked
    def version(cls, version: str, expected_version: str) -> bool:
        """Compares the version of the current platform and the version info in the spec file.

        TODO Works with both the platforms block and the modules block?
        TODO How to compare using the semver specification.
        TODO What about the modules which doesn't' use the semver spec?

        Uses the semver specification to compare.
        """
        if version == expected_version:
            return True
        return False
