# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:40:37 IST
# Last-Updated: Sun 23 Aug 2020 00:02:43 IST
#
# file_handler.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description: Handles everything file related
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

"""Includes "manager" for handling the `devfile` and your system files
"""
import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, cast

import anymarkup
import requests
from typeguard import typechecked

from devinstaller_core import common_models as m
from devinstaller_core import exception as e


class FileManager:
    """The "manager" for handling your system files."""

    @classmethod
    def read(cls, file_path: str) -> str:
        """Reads the file at the path and returns the string representation

        Args:
            file_path: The path to the file

        Returns:
            String representation of the file
        """
        full_path = os.path.expanduser(file_path)
        full_path_object = Path(full_path).resolve()
        try:
            with open(str(full_path_object), "r") as _f:
                return _f.read()
        except FileNotFoundError:
            raise e.FileNotFound

    @classmethod
    def download(cls, url: str) -> str:
        """Downloads file from the internet

        Args:
            url: Url of the file

        Returns:
            String representation of file
        """
        response = requests.get(url)
        return response.content.decode("utf-8")

    @classmethod
    def save(cls, file_content: str, file_path: str) -> None:
        """Downloads file from the internet and saves to file"""
        with open(file_path, "w") as f:
            f.write(file_content)

    @classmethod
    def hash_data(cls, input_data: str) -> str:
        """Hashes the input string and returns its digest"""
        return hashlib.sha256(input_data.encode("utf-8")).hexdigest()


class DevFileManager:
    """The `devfile` manager.

    Creates a object which contains the spec as Python object and its
    digest.

    Extraction methods:
        - *url* :  downloads the file
        - *file* : reads the file
        - *data* : returns the data as is

    Steps:
        1. Find the extraction method for the input
        2. Use the method to get the file
        3. hash the contents and returns the response object

    Args:
        file_path: path to file. Follows the spec format

    Raises:
        SpecificationError
            with error code :ref:`error-code-S101`. This is bubbled up by the `parse` method.

    Attributes:
        digest: Contains the SHA-256 hash of the contents
        contents: The Spec file Python object
    """

    pattern = r"^(url|file|data): (.*)"
    """pattern: This is the regex pattern used to parse the input path
    """

    fm = FileManager()
    """This is the object containing the file manager session
    """

    # hash_method: Callable[[str], str] = fm.hash_data
    """This method is used to hash the data
    """

    extract: Dict[str, Callable[[str], str]] = {
        "file": fm.read,
        "url": fm.download,
        "data": lambda x: x,
    }
    """This is a dict with all the methods that is used to extract the data
    """

    @typechecked
    def __init__(self, file_path: str) -> None:
        res = self.check_path(file_path)
        file_contents = self.extract[res.method](res.path)
        f = self.fm.hash_data
        if not callable(f):
            raise AttributeError(
                "I was expecting `hash_method` to be a function, but it is not."
            )
        self.digest = f(str(file_contents))
        self.contents = self.parse(file_contents)

    @classmethod
    @typechecked
    def check_path(cls, file_path: str) -> m.TypeCheckPathResponse:
        """Check if the given path is conforming to the spec.

        If it is complying with the specification then returns a dict
        with the `method` and the `path` which can be used to access
        the file.

        Args:
            file_path: The file path according to the spec

        Returns:
            Dict with `method` and `path`

        Raises:
            SpecificationError
                with code :ref:`error-code-S101`
        """
        try:
            result = re.match(cls.pattern, file_path)
            assert result is not None
            method = cast(m.TypeMethod, result.group(1))
            res = m.TypeCheckPathResponse(method=method, path=result.group(2))
            return res
        except AssertionError:
            raise e.SpecificationError(
                error=file_path,
                error_code="S101",
                message="The file_path you gave didn't start with a method.",
            )

    @typechecked
    def parse(self, file_contents: str, file_format: str = "toml") -> Dict[Any, Any]:
        """Parse `file_contents` and returns the python object

        Args:
            file_contents: The contents of file

        Returns:
            Python object

        Raises:
            SpecificationError
                with code :ref:`error-code-S100`
        """
        try:
            return anymarkup.parse(file_contents, format=file_format)
        except Exception:
            raise e.SpecificationError(
                error=file_contents,
                error_code="S100",
                message="There is some error in your file content",
            )
