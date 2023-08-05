from typing_extensions import Protocol
from viewdom import VDOM


class Component(Protocol):
    def __call__(self) -> VDOM:
        ...
