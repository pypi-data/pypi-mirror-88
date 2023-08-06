import sys
from typing import Optional, Union


class _Server:

    def __init__(self, ns: str, name: str) -> None:
        super().__init__()
        self.ns = ns
        self.name = name
        self.modules = sys.modules.copy()
        self.slot: Optional[Union[int, str]] = None


def register(ns: Optional[str], name: Optional[str]) -> _Server:
    return _Server(ns, name)
