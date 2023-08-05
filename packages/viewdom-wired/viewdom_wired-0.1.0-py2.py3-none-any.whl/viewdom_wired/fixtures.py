from dataclasses import dataclass
from typing import Protocol

import pytest
from viewdom import VDOM
from wired import ServiceRegistry, ServiceContainer
from wired.dataclasses import factory, register_dataclass


class Logo(Protocol):
    src: str
    alt: str

    def __call__(self) -> VDOM:
        ...


@dataclass
class Customer:
    name: str = 'Some Customer'


@factory()
@dataclass
class Settings:
    greeting: str = 'Hello'


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


@pytest.fixture
def customer() -> Customer:
    return Customer()


@pytest.fixture
def container(registry, customer) -> ServiceContainer:
    c = registry.create_container(context=customer)
    return c
