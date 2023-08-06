# -----------------------------------------------------------------------------
# Created: Thu 28 May 2020 23:37:47 IST
# Last-Updated: Sun 16 Aug 2020 16:53:34 IST
#
# models.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description: Contains all the app data
#
# Copyright (c) 2020, Justin Kizhakkinedath
# All rights reserved
#
# Licensed under the terms of The MIT License
# See LICENSE file in the project root for full information.
# -----------------------------------------------------------------------------
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "software"), to deal in the software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the software, and to permit
# persons to whom the software is furnished to do so, subject to the
# following conditions:
#
# the above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the software.
#
# the software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.
# in no event shall the authors or copyright holders be liable for any claim,
# damages or other liability, whether in an action of contract, tort or
# otherwise, arising from, out of or in connection with the software or the
# use or other dealings in the software.
# -----------------------------------------------------------------------------

"""All the models including the schema as well as graph models"""
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, TypedDict, Union

from devinstaller_core.module_app import ModuleApp
from devinstaller_core.module_file import ModuleFile
from devinstaller_core.module_folder import ModuleFolder
from devinstaller_core.module_group import ModuleGroup
from devinstaller_core.module_link import ModuleLink
from devinstaller_core.module_phony import ModulePhony


class TypeModuleInstallInstruction(TypedDict, total=False):
    """Type declaration for the instruction for `init`, `command` and `config`
    """

    cmd: str
    rollback: Optional[str]


class TypeCommonModule(TypedDict, total=False):
    """Type declaration for all the block
    """

    alias: str
    commands: List[Union[TypeModuleInstallInstruction, str]]
    install_inst: List[TypeModuleInstallInstruction]
    config: List[Union[TypeModuleInstallInstruction, str]]
    content: str
    create: bool
    description: str
    display: str
    executable: str
    init: List[Union[TypeModuleInstallInstruction, str]]
    module_type: str
    name: str
    optionals: List[str]
    owner: str
    parent_dir: str
    permission: str
    requires: List[str]
    rollback: bool
    source: str
    supported_platforms: List[str]
    symbolic: bool
    target: str
    url: str
    version: str
    before: Optional[str]
    after: Optional[str]


class TypeInterfaceModule(TypedDict, total=False):
    """Type declaration for the `modules` in the interface block
    """

    name: str
    before: str
    after: str


class TypeInterface(TypedDict, total=False):
    """Type declaration for the interface block
    """

    name: str
    description: str
    before: str
    after: str
    before_each: str
    after_each: str
    modules: List[TypeInterfaceModule]


class TypePlatformInfo(TypedDict, total=False):
    """Type declaration for the platform info
    """

    system: str
    version: str


class TypePlatform(TypedDict, total=False):
    """Type declaration for the `platform` block
    """

    name: str
    description: str
    platform_info: TypePlatformInfo


class TypePlatformInclude(TypedDict, total=False):
    """Type declaration for the platform include block
    """

    spec_file: str
    prog_file: str


class TypeFullDocument(TypedDict, total=False):
    """Type declaration for the whole spec file
    """

    version: str
    author: str
    description: str
    url: str
    prog_file: str
    include: List[TypePlatformInclude]
    platforms: List[TypePlatform]
    modules: List[TypeCommonModule]
    interfaces: List[TypeInterface]


class TypeValidateResponse(TypedDict):
    """Type declaration for the response of the `devinstaller.schema.validate` function
    """

    valid: bool
    document: Dict[Any, Any]
    errors: Dict[Any, Any]


TypeMethod = Literal["file", "url", "data"]


@dataclass
class TypeCheckPathResponse:
    """Type declaration for the response of the
    `devinstaller.file_manager.DevFileManager.check_path` method
    """

    method: TypeMethod
    path: str


TypeAnyModule = Union[
    ModuleApp, ModuleFile, ModuleFolder, ModuleLink, ModuleGroup, ModulePhony
]

TypeModuleMap = Dict[str, TypeAnyModule]

ModuleInstallStatus = ["success", "failed", "in progress"]
"""Status allowed for each modules. None is also included in Moduel status

Values allowed:
    1. `success`
    2. `failed`
    3. `in progress`
"""

ModuleInstallInstructionKeys = Literal["init", "commands", "config"]
"""These are the keys allowed for converting installation steps into
`ModuleInstallInstruction` object

Values allowed:
    1. `init`
    2. `commands`
    3. `config`
"""


def convert_to_instruction_dict(installation_str: str) -> Dict[str, str]:
    return {"cmd": installation_str}


def module() -> Dict[str, Any]:
    """
    Returns:
        The schema for the `module` block
    """
    data = {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "module_type": {
                    "type": "string",
                    "default": "phony",
                    "allowed": ["app", "file", "folder", "link", "group", "phony"],
                },
                "supported_platforms": {"type": "list", "schema": {"type": "string"}},
                "bind": {"type": "list", "schema": {"type": "string"}},
                "constants": {
                    "type": "list",
                    "schema": {
                        "key": {"type": "string", "required": True},
                        "value": {"type": "string", "required": True},
                    },
                },
                "alias": {"type": "string"},
                "create": {"type": "boolean"},
                "init": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "coerce": (str, convert_to_instruction_dict),
                        "schema": {
                            "cmd": {"type": "string", "required": True},
                            "rollback": {"type": "string"},
                        },
                    },
                },
                "install_inst": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "coerce": (str, convert_to_instruction_dict),
                        "schema": {
                            "cmd": {"type": "string", "required": True},
                            "rollback": {"type": "string"},
                        },
                    },
                },
                "config": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "coerce": (str, convert_to_instruction_dict),
                        "schema": {
                            "cmd": {"type": "string", "required": True},
                            "rollback": {"type": "string"},
                        },
                    },
                },
                "commands": {"type": "list", "schema": {"type": "string"}},
                "uninstall_inst": {"type": "list", "schema": {"type": "string"}},
                "content": {
                    "type": "dict",
                    "schema": {
                        "digest": {"type": "string"},
                        "path": {"type": "string"},
                    },
                },
                "description": {"type": "string"},
                "display": {"type": "string"},
                "executable": {"type": "string"},
                "name": {"type": "string", "required": True},
                "optionals": {"type": "list", "schema": {"type": "string"}},
                "owner": {"type": "string"},
                "parent_dir": {"type": "string"},
                "permission": {"type": "string"},
                "requires": {"type": "list", "schema": {"type": "string"}},
                "url": {"type": "string"},
                "version": {"type": "string", "coerce": str},
                "source": {"type": "string"},
                "target": {"type": "string"},
                "symbolic": {"type": "boolean"},
            },
        },
    }
    return data


def platform() -> Dict[str, Any]:
    """
    Returns:
        The schema for the `platform` block
    """
    data = {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string", "required": True},
                "description": {"type": "string"},
                "platform_info": {
                    "type": "dict",
                    "schema": {
                        "system": {"type": "string", "required": True},
                        "version": {"type": "string", "coerce": str},
                    },
                },
            },
        },
    }
    return data


def interface() -> Dict[str, Any]:
    """
    Returns:
      The schema for the `interface` block
    """
    data = {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string", "required": True},
                "description": {"type": "string"},
                "before": {"type": "string"},
                "after": {"type": "string"},
                "before_each": {"type": "string"},
                "after_each": {"type": "string"},
                "modules": {
                    "type": "list",
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "name": {"type": "string"},
                            "before": {"type": "string"},
                            "after": {"type": "string"},
                        },
                    },
                },
            },
        },
    }
    return data


def constant() -> Dict[str, Any]:
    """
    Returns:
        Schema for validating the `constant` block
    """
    data = {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "name": {"type": "string", "required": True},
                "inherit": {"type": "list", "schema": {"type": "string"}},
                "data": {
                    "type": "list",
                    "schema": {
                        "key": {"type": "string", "required": True},
                        "value": {"type": "string", "required": True},
                    },
                },
            },
        },
    }
    return data


def top_level() -> Dict[str, Any]:
    """
    Returns:
        Schema for validating the top level block
    """
    data = {
        "version": {"type": "string", "coerce": str},
        "author": {"type": "string"},
        "description": {"type": "string"},
        "url": {"type": "string"},
        "include": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "spec_file": {"type": "string", "required": True},
                    "prog_file": {"type": "string"},
                },
            },
        },
        "prog_file": {"type": "string"},
    }
    return data


def schema() -> Dict[str, Any]:
    """Used for getting a new instance of the schema for the validating the spec file.

    Returns:
      The schema for the whole spec
    """
    data = dict(**top_level())
    data["constants"] = constant()
    data["platforms"] = platform()
    data["modules"] = module()
    data["interfaces"] = interface()
    return data
