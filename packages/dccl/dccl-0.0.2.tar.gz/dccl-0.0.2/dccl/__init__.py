from typing import Any, Generator, Optional, Union


NS_STANDARD = "standard"

TOOL_HOUDINI = "houdini"
TOOL_CINEMA4D = "cinema4d"
TOOL_MAYA = "maya"
TOOL_3DSMAX = "3dsmax"
TOOL_BLENDER = "blender"


class _Client:

    def __init__(self, ns: str, tool: str, port: int) -> None:
        super().__init__()
        self.ns = ns
        self.tool = tool
        self.port = port

    # Runs a script file in the remote instance.
    def exec_file(self, path: str, type: str = "py", wait: bool = True, bg: bool = False) -> Any:
        pass

    # Executes script code in the remote instance.
    def exec_code(self, code: str, type: str = "py", wait: bool = True, bg: bool = False) -> Any:
        pass

    # Determines a module of the remote instance and returns a proxy object.
    def module(self, name: str, type: str = "py", bg: bool = False) -> Any:
        pass


class _Registry:

    def __init__(self, ns: str, tool: str) -> None:
        super().__init__()
        self.ns = ns
        self.tool = tool

    # Determines an active instance by slot number or slot name. If the instance
    # is not found, it will automatically ask for a suitable instance if the
    # fallback parameter is set.
    def get(self, slot: Union[int, str], ask: Union[bool, str] = False) -> _Client:
        pass

    # Asks the user which active instance should be selected. The specified
    # description text is displayed here.
    def ask(self, descr: Optional[str]) -> Optional[_Client]:
        pass

    # Returns a list of all active instances.
    def list(self) -> list[_Client]:
        pass

    # Opens the installation manager window, which lists found DCC installations
    # and allows an extension to be installed. If no extension is specified, the
    # default extension is installed.
    def install(self, ext_path: Optional[str]) -> None:
        pass


class _Namespace:

    def __init__(self, ns: str) -> None:
        super().__init__()
        self.hou = _Registry(ns, TOOL_HOUDINI)
        self.c4d = _Registry(ns, TOOL_CINEMA4D)
        self.maya = _Registry(ns, TOOL_MAYA)
        self.max = _Registry(ns, TOOL_3DSMAX)
        self.blend = _Registry(ns, TOOL_BLENDER)


standard = _Namespace(NS_STANDARD)
hou = standard.hou
c4d = standard.c4d
maya = standard.maya
max = standard.max
blend = standard.blend
