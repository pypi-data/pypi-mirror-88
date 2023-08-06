"""All the constants in library
"""


class SessionSpec:
    """All the constants for the `SessionSpec`
    """

    EXTENSION_CLASS = "ExtSpec"
    BUILTIN_EXTENSIONS = [
        "devinstaller_core.command_python",
        "devinstaller_core.command_shell",
    ]
    PARSE_PATTERN = r"^(.*): (.*)"


class SessionProg:
    """All the constants for the `SessionProg`
    """

    EXTENSION_CLASS = "ExtProg"
    BUILTIN_EXTENSIONS = ["devinstaller_core.command_python"]


class UserInteraction:

    EXTENSION_CLASS = "ExtUserInteraction"
    BUILTIN_EXTENSIONS = ["devinstaller_core.user_interaction"]
