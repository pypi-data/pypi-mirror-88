"""The Module for creating extensions
"""
import importlib
import pkgutil
from abc import ABC, abstractmethod
from typing import Any, Generic, List, TypeVar, cast

from devinstaller_core import exception as e


class BaseExt(ABC):
    """Base class for creating Abstract class for Extensions

    Warning:
        Don't inherit this class for creating any Extensions.
        This class is for creating other classes which is what you need to create
        base class for Extensions.
    """


class BaseExtApplication(BaseExt):
    """Base extension class for creating extentions for the application
    """


class BaseExtLang(BaseExt):
    """Base class for creating Extensions for different programming languages

    Warning:
        Don't inherit this class for creating Extensions for supporting different
        programming languages.

    See Also:
        - :class:`.ExtSpec`
        - :class:`.ExtProg`
    """

    @property
    @abstractmethod
    def LANGUAGE_CODE(self):
        """The language code
        """

    @property
    @abstractmethod
    def LANGUAGE_NAME(self):
        """The name of the programming language
        """


class ExtSpec(BaseExtLang):
    """Base class for creating Extensions for running commands in spec file

    This is used to create programming language extensions to run commands
    in spec file.
    """

    @abstractmethod
    def run(self, command: str) -> None:
        """Run the given `command` in the interpretor
        """


class ExtProg(BaseExtLang):
    """Base class for creating Extensions for executing prog files

    This is used to create programming language extensions to run
    commands in the prog file.
    """

    @abstractmethod
    def launch(self, launch: str) -> None:
        """Execute the given `launch` attribute using the prog module
        """


class ExtUserInteraction(BaseExtApplication):
    """Extension class for creating extensions for the user interaction facility
    """

    @abstractmethod
    def select(self, title: str, choices: List[str]) -> str:
        """Ask user to select a option from the given choices

        Returns:
            The selected choice
        """

    @abstractmethod
    def print(self, message: Any) -> None:
        """Prints the given object to the console in rich-text format
        """

    @abstractmethod
    def checkbox(self, title: str, choices: List[str]) -> List[str]:
        """Ask user to select one or more choices"""

    @abstractmethod
    def confirm(self, title: str) -> bool:
        """Ask user to confirm a decision"""


ExtensionModule = TypeVar("ExtensionModule", bound=BaseExt)


class BaseExtension(Generic[ExtensionModule], ABC):
    """Base class for importing extensions"""

    def __init__(self, builtin_extensions: List[str], ext_class: str) -> None:
        """

        Args:
            builtin_extensions: The list of all the builtin extensions
            ext_class: The name of the class which will be imported and
                used
        """
        self.extensions = builtin_extensions
        self.ext_class = ext_class
        for finder, name, ispkg in pkgutil.iter_modules():
            if name.startswith("devinstaller_ext_"):
                self.extensions.append(name)
        for ext_path in self.extensions:
            ext = self.import_ext(ext_path, self.ext_class)
            self.load_extension(ext)

    @abstractmethod
    def load_extension(self, extension: ExtensionModule):
        """Logic for loading the extension

        This method recieves the Extension class parsed and ready to be loaded.

        It is how you inherit and define this method the Extension will be loaded.
        """

    @classmethod
    def import_ext(cls, module_path: str, ext_class_name: str) -> ExtensionModule:
        """Import Extension using the name of the module and the class where it is defined

        Returns:
            Instance of the class
        """
        module = importlib.import_module(module_path)
        ext_class = getattr(module, ext_class_name)
        try:
            assert issubclass(ext_class, BaseExt)
            return ext_class()
        except AssertionError:
            raise e.DevinstallerError(ext_class, "D102")
