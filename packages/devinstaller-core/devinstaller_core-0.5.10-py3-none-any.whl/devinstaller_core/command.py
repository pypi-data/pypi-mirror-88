# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 16:55:05 IST
# Last-Updated: Tue 24 Nov 2020 15:44:35 IST
#
# commands.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description: Handles all the required logic to run shell commands
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

"""Handles everything related to running shell commands"""
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Generic, List, TypeVar, cast

from devinstaller_core import constants as c
from devinstaller_core import exception as e
from devinstaller_core import extension as ex


@dataclass
class CommandResponse:
    """Response object for the `devinstaller.comands.check_cmd`

    parameters:
        prog: The language code of the programming language used
        cmd: The actual command to be run
    """

    prog: str
    cmd: str


class SessionSpec(ex.BaseExtension[ex.ExtSpec]):
    """Using this class you can create a session object for running
    commands in spec file

    Create a session using this class and use the `run` method to run the commands
    """

    def __init__(self) -> None:
        ext_class = c.SessionSpec.EXTENSION_CLASS
        builtin_extensions = c.SessionSpec.BUILTIN_EXTENSIONS
        self.prog: Dict[str, ex.ExtSpec] = {}
        super().__init__(builtin_extensions=builtin_extensions, ext_class=ext_class)

    def run(self, command: str) -> None:
        """Run shell or python command

        Examples:
            - run(`'sh: echo "Hello world"'`)
            - run(`'py: print("Hello world")'`)

        Args:
            command: The full spec based command string
        """
        res: CommandResponse = self.parse(command)
        lang_obj = self.prog[res.prog]
        lang_obj.run(res.cmd)

    @classmethod
    def parse(cls, command: str) -> CommandResponse:
        """Check the command and returns the command response object"""
        # try:
        pattern = c.SessionSpec.PARSE_PATTERN
        result = re.match(pattern, command)
        if result is None:
            return CommandResponse(prog=c.SessionSpec.DEFAULT_LANG, cmd=command)
        return CommandResponse(prog=result.group(1), cmd=result.group(2))
        # except AssertionError:
        #     raise e.SpecificationError(
        #         error=command,
        #         error_code="S100",
        #         message="The command didn't conform to the spec",
        #     )

    def load_extension(self, extension: ex.ExtSpec):
        """Loading extension"""
        self.prog[extension.LANGUAGE_CODE] = extension


class SessionProg(ex.BaseExtension[ex.ExtProg]):
    """Create a session for executing prog files"""

    def __init__(self) -> None:
        ext_class = c.SessionProg.EXTENSION_CLASS
        builtin_extensions = c.SessionProg.BUILTIN_EXTENSIONS
        self.prog: Dict[str, ex.ExtProg] = {}
        super().__init__(builtin_extensions=builtin_extensions, ext_class=ext_class)

    def launch(
        self, function_name: str, prog_file_path: str, language_code: str = "py"
    ) -> None:
        pass

    def load_extension(self, extension: ex.ExtProg):
        """Loading extension"""
        self.prog[extension.LANGUAGE_CODE] = extension
