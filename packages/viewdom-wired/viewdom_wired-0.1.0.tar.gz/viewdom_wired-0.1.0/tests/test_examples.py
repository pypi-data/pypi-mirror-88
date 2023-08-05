import pytest

from examples import (
    hello_world,
    hello_children,
    hello_app,
    app_plugin_site,
    app_decorators_render,
    subcomponents,
    override,
    context,
    custom_context,
    protocols_hello_logo,
    logo_protocol,
    adherent,
)


@pytest.mark.parametrize(
    'target',
    [
        hello_world,
        hello_children,
        hello_app,
        app_plugin_site,
        app_decorators_render,
        subcomponents,
        override,
        context,
        custom_context,
        protocols_hello_logo,
        logo_protocol,
        adherent,
    ],
)
def test_examples(target):
    expected, actual = target.test()
    assert expected == actual
