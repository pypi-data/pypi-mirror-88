from devinstaller_core import extension as ex

CODE = "py"
NAME = "Python"


class ExtSpec(ex.ExtSpec):
    LANGUAGE_CODE = CODE
    LANGUAGE_NAME = NAME

    def run(self, command: str):
        """Execute the given string in python
        """
        exec(command)


class ExtProg(ex.ExtProg):
    LANGUAGE_CODE = CODE
    LANGUAGE_NAME = NAME

    def launch(self, python_fun_name: str):
        pass
