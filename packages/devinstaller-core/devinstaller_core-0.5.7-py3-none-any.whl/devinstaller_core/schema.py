# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:12:48 IST
# Last-Updated: Sun 16 Aug 2020 16:54:07 IST
#
# schema.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description:
#
# Copyright (c) 2020, Justine Kizhakkinedath
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

"""Handles everything related to spec file schema"""
from typing import Any, Dict, cast

import cerberus
from typeguard import typechecked

from devinstaller_core import common_models as cm
from devinstaller_core import exception as e


@typechecked
def validate(
    document: Dict[Any, Any], schema: Dict[Any, Any]
) -> cm.TypeValidateResponse:
    """Check if the given document is valid or not

    Args:
        document: Python object which has to be validated
        schema: Schema to check for its validity

    Returns:
        A dict with its validity, document and its errors.
    """
    _v = cerberus.Validator(schema)
    data: cm.TypeValidateResponse = {
        "valid": _v.validate(document),
        "document": _v.document,
        "errors": _v.errors,
    }
    return data


@typechecked
def get_validated_document(document: Dict[Any, Any]) -> cm.TypeFullDocument:
    """Validate the given document against the Devinstaller specification

    Args:
        document: Python object which has to be validated

    Returns:
        Validated object

    Raises:
        SpecificationError
            with error code :ref:`error-code-S100`
    """
    data = validate(document, schema=cm.schema())
    if data["valid"]:
        d = cm.TypeFullDocument(data["document"])
        return d
    raise e.SpecificationError(str(data["errors"]), "S100")
