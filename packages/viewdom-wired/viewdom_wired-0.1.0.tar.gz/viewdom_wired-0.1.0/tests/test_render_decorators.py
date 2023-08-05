"""

Test usage of wired and components via decorators instead of
imperative.

More cumbersome (due to scanner) to copy around so placed into a
single test.

"""
from dataclasses import dataclass

import pytest
from viewdom.h import html
from wired import ServiceRegistry
from wired.dataclasses import factory, register_dataclass
from wired_injector import injectable
from wired_injector.operators import Attr, Context, Get

from viewdom_wired import render

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore


class FirstContext:
    def __init__(self):
        self.name = 'First Context'


class SecondContext:
    def __init__(self):
        self.name = 'Second Context'


@factory()
@dataclass
class Settings:
    greeting: str = 'Hello'


@injectable()
@dataclass
class Heading:
    person: str
    name: Annotated[str, Context(), Attr('name')]
    greeting: Annotated[str, Get(Settings), Attr('greeting')]

    def __call__(self):
        return html('''<h1>{self.greeting} {self.person}, {self.name}</h1>''')


@pytest.fixture
def registry() -> ServiceRegistry:
    import sys
    from venusian import Scanner

    registry = ServiceRegistry()
    scanner = Scanner(registry=registry)
    current_module = sys.modules[__name__]
    scanner.scan(current_module)
    register_dataclass(registry, Settings)
    return registry


@injectable(for_=Heading, context=SecondContext)
@dataclass
class SecondHeading:
    person: str
    name: Annotated[str, Context(), Attr('name')]
    greeting: Annotated[str, Get(Settings), Attr('greeting')]

    def __call__(self):
        return html(
            '''
        <h1>{self.greeting} {self.person}... {self.name}</h1>
        '''
        )


def test_wired_renderer_first(registry: ServiceRegistry):
    container = registry.create_container(context=FirstContext())
    expected = '<h1>Hello World, First Context</h1>'
    actual = render(html('''<{Heading} person="World"/>'''), container)
    assert expected == actual


def test_wired_renderer_second(registry: ServiceRegistry):
    container = registry.create_container(context=SecondContext())
    expected = '<h1>Hello World... Second Context</h1>'
    actual = render(html('''<{Heading} person="World"/>'''), container)
    assert expected == actual
