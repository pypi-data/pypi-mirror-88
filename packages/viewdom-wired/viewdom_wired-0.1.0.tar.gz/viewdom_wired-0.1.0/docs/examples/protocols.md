# Protocols


In [](./examples/classes we saw how to provide different flavors of components, using `for_` to establish the relationship.
This solves the registration problem, but other parts of your code don't know that `SiteGreeter` is a kind of `Greeter`.

While we could use subclassing, sharing the implementation has downsides.
Python's `PEP 544 <https://www.python.org/dev/peps/pep-0544/>`_ uses "protocols" and *structural* subtyping.
With this, different implementations of `Greeting` can adhere to a contract, and tools such as `mypy` can enforce it.
Fortunately, `wired` can use protocols in the `for_` to register implementations.

Let's write an application showing the use of protocols in a component system.

## hello_logo

We have a pluggable app that ships with its own components: a `Navbar` which has a `Logo` subcomponent.
The app changes slightly to scan the `components.py` module for registrations:

```{literalinclude} ../../examples/protocols_hello_logo/app/app.py
---
start-after: from venusian
---
```

The two built-in components:

```{literalinclude} ../../examples/protocols_hello_logo/app/components.py
---
start-after: from wired_injector
---
```

The site is using a plugin which replaces the built-in logo with one that allows an `alt` value:

```{literalinclude} ../../examples/protocols_hello_logo/plugins/logo/components.py
---
start-after: from wired_injector
---
```

The site has a view with a template which renders a `Navbar`:

```{literalinclude} ../../examples/protocols_hello_logo/site/views.py
---
start-after: from viewdom
---
```

The result is `'<nav><img src="logo.png" alt="Logo"/></nav>'`.

Sure, the tests pass.
But `NoAltLogo` isn't a kind of `Logo`.
Someone else might use it, try to pass in an `alt`, and fail.

We could solve this with subclassing.
But as PEP 544 points out, the world of Python has learned the hazards of sharing implementation.
Is there some other way to say `NoAltLogo` is a kind of `Logo` and have Python static typing tell us when contracts are broken?

## Protocols

First, let's break the concept from the implementation: `Logo` will be a PEP 544 protocol.

The pluggable app will define the `Logo` protocol then provide a `DefaultLogo` implementation of that protocol:

```{literalinclude} ../../examples/logo_protocol/plugins/logo/components.py
---
start-after: from wired_injector
---
```

The `NoAltLogo` component in the plugin doesn't need to change.
But when it says it is `for_=Logo`, it's "for" a protocol, not a particular implementation of that protocol.

This all works well, because `wired` just treats `Logo` as a marker, whether a class or a "protocol".

However, we still don't have a way to say `NoAltLogo` is a `Logo`, much less enforce it with `mypy`.
In fact, the type checker now gets mad on this line:

```python
logo: Logo = NoAltLogo(src='alt.png')
```

...because `NoAltLogo` is not a type of `Logo`.

## adherent

In the `mypy` tracker, Glyph `pointed to a decorator <https://github.com/python/mypy/issues/4717#issuecomment-454609539>`_ which could say "the following class implements a certain protocol."
Let's use it.

```{literalinclude} ../../examples/adherent/app/decorators.py
---
start-at: protocol =
---
```

The built-in `DefaultLogo` needs to say it adheres to the `Logo` protocol:

```{literalinclude} ../../examples/adherent/app/components.py
---
start-at: injectable(for_=Logo)
---
```

The plugin's component needs to adhere as well:

```{literalinclude} ../../examples/adherent/plugins/logo/components.py
---
start-at: injectable(for_=Logo)
---
```

Unlike `zope.interface`, `mypy` won't immediately validate conformance.
You have to use the component somewhere.
Since Python doesn't really know about tagged templates, it doesn't treat it like an f-string (a problem to be solved later.)
But any instance creation in a test, as we've done when testing VDOMs, would get an error from `mypy` if it was pointed at the tests.

Unfortunately the error message from `mypy` is not as rich as that of `zope.interface` verification.
It doesn't tell you how the adherent failed, just that it failed.

## Futures

It's an interesting direction to consider. What could be improved with the use of protocols?

- Conflate the `adherent` and `component` decorator to avoid double-typing

- Either have Python adopt tagged templates or teach type checkers to treat `html('{self.src}')` as an f-string

- Go further and teach type checkers and IDEs to autocomplete and r ed-squiggly on adherents

- Also teach them to navigate to protocols, then from there to implementations (similar to superclasses and usages)
