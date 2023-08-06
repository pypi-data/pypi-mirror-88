"""The main module which is used by CLI and Library
"""
import importlib.util
import os
import tempfile
import types
from importlib.abc import Loader
from typing import Any, Callable, Dict, List, Optional, Set

from typeguard import typechecked

from devinstaller_core import block_platform as bp
from devinstaller_core import common_models as m
from devinstaller_core import dependency_graph as dg
from devinstaller_core import exception as e
from devinstaller_core import file_manager as f
from devinstaller_core import schema as s
from devinstaller_core.utilities import ui

# dfm = f.DevFileManager()
fm = f.FileManager()


@typechecked
def load_devfile(
    schema_object: m.TypeFullDocument, prog_file_path: Optional[str] = None
) -> types.ModuleType:
    """Loads the file and returns the module

    Args:
        schema_object: The full schema object
        prog_file_path: The path to the `prog_file`

    Returns:
        The module
    """
    if prog_file_path is None:
        prog_file_path = schema_object["prog_file"]
    res: m.TypeCheckPathResponse = f.DevFileManager.check_path(prog_file_path)
    file_functions: Dict[str, Callable[[str], str]] = {
        "file": lambda path: path,
        "url": download_devfile,
        "data": download_devfile,
    }
    module_path = file_functions[res.method](res.path)
    dev_module = load_python_module(module_path)
    if res.method == "url" or res.method == "data":
        os.remove(module_path)
    return dev_module


@typechecked
def download_devfile(file_path: str) -> str:
    """Downloads the devfile so that it can be loaded

    Args:
        file_path: The path to the file

    Returns:
        The path where the file is saved
    """
    temp = fm.read(file_path=file_path)
    temp_file_path = tempfile.mkstemp()[1]
    fm.save(temp, file_path=temp_file_path)
    return temp_file_path


@typechecked
def load_python_module(
    file_path: str, module_name: str = "devfile"
) -> types.ModuleType:
    """Loads the module
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    assert isinstance(spec.loader, Loader)
    spec.loader.exec_module(module)
    return module


@typechecked
def create_dependency_graph(
    schema_object: m.TypeFullDocument, platform_codename: Optional[str]
) -> dg.DependencyGraph:
    platform_object = get_platform_object(
        full_document=schema_object, platform_codename=platform_codename
    )
    dependency_graph = dg.DependencyGraph(
        module_list=schema_object["modules"], platform_object=platform_object
    )
    return dependency_graph


@typechecked
def core(
    file_path: Optional[str] = None, spec_object: Optional[Dict[Any, Any]] = None
) -> m.TypeFullDocument:
    """The core function.

    Validates and returns the schema object.
    """
    if file_path is not None:
        dfm = f.DevFileManager(file_path)
        schema_object: Dict[Any, Any] = dfm.contents
    elif spec_object is not None:
        schema_object = spec_object
    else:
        raise e.DevinstallerError("Schema object not found", "D100")
    res = s.get_validated_document(schema_object)
    return res


@typechecked
def get_platform_object(
    full_document: m.TypeFullDocument, platform_codename: Optional[str] = None
) -> bp.BlockPlatform:
    """Create the platform object and return it
    """
    platform_list = full_document.get("platforms", None)
    platform_object = bp.BlockPlatform(
        platform_list=platform_list, platform_codename=platform_codename
    )
    return platform_object


@typechecked
def get_requirement_list(module_objects: List[m.TypeAnyModule],) -> List[str]:
    """Ask the user for which modules to be installed

    Args:
        module_objects: List of all the modules you want to display to the user

    Returns:
        List of the objects of all the modules to be installed.
    """
    ui.print("Hey... You haven't selected which module to be installed")
    title = "Do you mind selected a few for me?"
    choices = {str(mod): mod for mod in module_objects}
    selections = ui.checkbox(title, choices=list(choices.keys()))
    data: List[str] = []
    for _s in selections:
        _m = choices[_s]
        assert _m.alias is not None
        data.append(_m.alias)
    return data


@typechecked
def get_user_confirmation(orphan_list: Set[str]) -> bool:
    """Asks user for confirmation for the uninstallation of the orphan modules.

    Args:
        orphan_list: The "list" of modules which are not used by any other modules
    """
    ui.print(
        "Because of failed installation of some modules, there are some"
        "modules which are installed but not required by any other modules"
    )
    orphan_module_names = ", ".join(name for name in orphan_list)
    ui.print(f"These are the modules: {orphan_module_names}")
    response = ui.confirm("Do you want to uninstall?")
    return response
