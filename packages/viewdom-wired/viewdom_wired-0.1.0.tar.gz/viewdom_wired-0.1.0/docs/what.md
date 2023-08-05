# What It Is

The world of modern frontends have adopted several patterns that help scale UI development, primarily components and related efforts such as a context API and hooks.
``viewdom_wired`` is part of a multi-layered effort to bring that style and those benefits to Python web development:

- [tagged](https://github.com/jviide/tagged) emulates [JavaScript tagged templates[(https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals)

- [htm.py](https://github.com/jviide/htm.py) is a Python port of the innovative, successful [htm](https://github.com/developit/htm) package ("JSX-like syntax in plain JavaScript - no transpiler necessary")

- [viewdom](https://viewdom.readthedocs.io/en/latest/) is a Python-side renderer for VDOMs from `htm.py`

- [wired](https://wired.readthedocs.io/en/latest/) provides dependency injection for easily-replaceable parts

There are layers planned atop `viewdom_wired` for opinionated and ready-to-go UIs.

## Pluggability

- Assemble a site from apps and plugins
- Small units of isolated *replaceability*

With `viewdom_wired`, a [pluggable app](./pluggable) manages a `wired.ServiceRegistry`.
The app, any extensions, and site customizations can then register things in that registry, including both variations and overrides.
Then, during some operation such as processing a request, a container is made, from which instances are created and stored.

Translation? You can make an `Image` component for `htm.py`.
Then, when a template asks for `Image`, the actual implementation comes from the registry, not a single built-in implementation.
The container might hand over an `Image`:

- From the default, built-in `Image`

- An `Image` from the theme that's in use, which overrode the built-in Image

- The site might have a variation of `Image` when a `MobileCustomer` is the container's context

## Injection

- Instead of passing data down long tree as props...
- Components can ask for data from environment

For the `Image` scenario, them default component might look like this:

```python
@component()
@dataclass
class Image:
    src: str
    is_responsive: bool = injected(SiteConfig, attr="use_responsive")

    def __html__(self):
        if is_responsive:
            return html('<img src={self.src} blah blah'/>)
        return html('<img src={self.src}/>')
```

It could be used in another component as such:

```python
from mypackage import Image
html('<{Image} src={this_image} />')
```

This passes the `src` prop but not `is_responsive`, because `Image` defaults to asking the injector to retrieve that value from the site configuration.

This is *really* nice:

- `SiteConfig` doesn't have to be passed through tons of intermediate components who don't need it, but have to ship it to a great-great-grandchild

- If `Image` wants something else from `SiteConfig`, it doesn't need a new prop, and thus doesn't break the universe of callers

A neat aspect of doing it this dataclass-y way:

```
<{Image} src={this_image} is_responsive={False} />
```

Because the `wired` DI lets you specify just an attr, an individual usage of an `Image` can pass in a prop that supercedes the injection.

## Context-Specific Components

- Use a built-in component most of the time
- Pick a different implementation in specific cases

In `wired`, you can register different flavors of a service, each for use with a particular "context".
Then, when making a container, you provide the context used for the lookups during the life of that container.

This means you can have context-specific `Image` components.
For example, we could have a second registration of an image:

```python
@component(context=MobileCustomer)
@dataclass
class MobileImage:
    src: str
    is_responsive: bool = injected(SiteConfig, attr="use_responsive")

    def __html__(self):
        if is_responsive:
            # Some markup/logic
            return html('<img src={self.src} blah blah'/>)
        # Etc.
        return html('<img src={self.src}/>')
```

The pluggable app would construct, e.g. for each request, a container with whatever is the correct context:

```python
customer_id = request.url('blah blah')
context = MobileCustomer(id=customer_id)
container = registry.create_container(context=context)
```

From that point on, neither the callers (a usage of a component in a template) nor the callees (the dataclasses that implement that component) need to change to handle this extra case.
It becomes a very powerful way for specific customization without forking.

The users of `Image` don't know they are getting a different *implementation*.
They are just asking for a marker/interface/protocol, so the same import still works, but uses `MobileImage`:

```python
from mypackage import Image
html('<{Image} src={this_image} />')
```
