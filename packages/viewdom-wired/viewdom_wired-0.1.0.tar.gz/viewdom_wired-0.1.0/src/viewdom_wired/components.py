"""
General-purpose components useful in all viewdom_wired apps.

"""
from dataclasses import dataclass

from viewdom import VDOM


@dataclass
class Super:
    parent_children: VDOM = ()

    def __call__(self) -> VDOM:
        return self.parent_children
