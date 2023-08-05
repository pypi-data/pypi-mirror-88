from dataclasses import dataclass
from typing import Tuple

import pytest
from viewdom.h import html
from wired import ServiceRegistry
from wired.dataclasses import factory, register_dataclass
from wired_injector import injectable
from wired_injector.decorators import register_injectable
from wired_injector.operators import Context, Attr, Get

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
    name: Annotated[
        str,
        Context(),
        Attr('name'),
    ]
    greeting: Annotated[
        str,
        Get(Settings),
        Attr('greeting'),
    ]

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
    name: Annotated[
        str,
        Context(),
        Attr('name'),
    ]
    greeting: Annotated[
        str,
        Get(Settings),
        Attr('greeting'),
    ]

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


def test_wired_renderer_children(registry: ServiceRegistry):
    @dataclass
    class Heading2:
        children: str
        name: str = 'Hello'

        def __call__(self):
            return html('''<h1>{self.name}</h1><div>{self.children}</div>''')

    registry = ServiceRegistry()
    register_injectable(registry, Heading, Heading2)
    container = registry.create_container()
    expected = '<h1>Hello</h1><div>Child</div>'
    actual = render(html('''<{Heading}>Child<//>'''), container)
    assert expected == actual


def test_wired_renderer_generics(registry: ServiceRegistry):
    """ Tolerate usage of PEP 484 generics on type hints """

    @dataclass
    class LocalHeading:
        names: Tuple[str, ...] = ('Name 1',)

        def __call__(self):
            name_one = self.names[0]  # noqa: F841
            return html('<h1>{name_one}</h1>')

    container = registry.create_container()
    register_injectable(registry, LocalHeading, LocalHeading)
    expected = '<h1>Name 1</h1>'
    actual = render(html('''<{LocalHeading}/>'''), container)
    assert expected == actual
