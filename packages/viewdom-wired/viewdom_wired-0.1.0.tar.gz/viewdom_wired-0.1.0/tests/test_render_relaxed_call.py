"""
The component renderer uses a variation of wired's dataclass dependency
injector. Write some tests that cover policies.

"""
from dataclasses import dataclass

import pytest
from viewdom import html, VDOM
from wired_injector.decorators import register_injectable
from wired_injector.injector import Injector
from wired_injector.operators import Context, Attr

from viewdom_wired.fixtures import Customer

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated  # type: ignore

pytest_plugins = [
    'viewdom_wired.fixtures',
]


class Person:
    """ A marker class """

    pass


@pytest.fixture
def injector(container) -> Injector:
    injector = Injector(container)
    return injector


def test_str_default_value(registry, injector):
    """ Simple type (str) and has a default """

    @dataclass
    class TestPerson:
        name: str = 'default'

        def __call__(self) -> VDOM:
            return html('<div>{self.name}</div>')

    register_injectable(registry, for_=Person, target=TestPerson)
    person: TestPerson = injector(TestPerson)
    assert 'default' == person.name


def test_str_prop(registry, injector):
    """ Simple type (str) with passed-in value """

    @dataclass
    class TestPerson:
        name: str = 'default'

        def __call__(self) -> VDOM:
            return html('<div>{self.name}</div>')

    register_injectable(registry, for_=Person, target=TestPerson)
    person: TestPerson = injector(TestPerson, name='passed in')
    assert 'passed in' == person.name


def test_context(registry, injector):
    """ Use the type-hint to inject the context """

    @dataclass
    class TestPerson:
        customer: Annotated[
            Customer,
            Context(),
        ]

        def __call__(self) -> VDOM:
            return html('<div>{self.customer.name}</div>')

    register_injectable(
        registry, for_=Person, target=TestPerson, context=Customer
    )
    person = injector(TestPerson)
    assert 'Some Customer' == person.customer.name


def test_injected_attr(registry, injector):
    """ Used ``injected`` to get the context and grab an attr """

    @dataclass
    class TestPerson:
        name: Annotated[
            str,
            Context(),
            Attr('name'),
        ]

        def __call__(self) -> VDOM:
            return html('<div>{self.name}</div>')

    register_injectable(registry, for_=Person, target=TestPerson)
    person = injector(TestPerson)
    assert 'Some Customer' == person.name
