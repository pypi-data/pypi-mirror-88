from viewdom import Context
from viewdom.h import flatten, escape, encode_prop, VDOMNode, VOIDS
from wired import ServiceContainer
from wired_injector.injector import Injector


def relaxed_call(
    injector: Injector,
    callable_,
    children=None,
    parent_component=None,
    **kwargs,
):
    """ Make a component instance then call its __call__, returning a VDOM """

    target = injector.container.get(callable_)
    system_props = dict(children=children, parent_component=parent_component)
    component = injector(target, system_props=system_props, **kwargs)
    return component


def render(value, container: ServiceContainer, **kwargs):
    injector = Injector(container)
    return "".join(
        render_gen(
            Context(value, **kwargs),
            injector=injector,
            children=None,
            parent_component=None,
        )
    )


def render_gen(
    value, injector: Injector, children=None, parent_component=None
):
    for item in flatten(value):
        if isinstance(item, VDOMNode):
            tag, props, children = item.tag, item.props, item.children
            if callable(tag):
                component = relaxed_call(
                    injector,
                    tag,
                    children=children,
                    parent_component=parent_component,
                    **props,
                )
                parent_component = component
                yield from render_gen(
                    component(), injector, children, parent_component
                )
                continue

            yield f"<{escape(tag)}"
            if props:
                pi = props.items()
                yield f" {' '.join(encode_prop(k, v) for (k, v) in pi)}"

            if children:
                yield ">"
                yield from render_gen(
                    children, injector, parent_component=parent_component
                )
                yield f'</{escape(tag)}>'
            elif tag.lower() in VOIDS:
                yield '/>'
            else:
                yield f'></{tag}>'
        elif item not in (True, False, None):
            yield escape(item)
