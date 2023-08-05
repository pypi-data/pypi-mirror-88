# viewdom_wired: Container and DI for ``viewdom``

*Pluggability for Templates and Components*

Let's say you share some nice components.
You want them to work in different systems: Sphinx, Pelican, Flask, etc.
You also want to make it easy to extend or customize without having to fork.

`viewdom_wired` brings pluggability and flexibility to [viewdom](https://viewdom.readthedocs.io/en/latest/) templates and components.
With dependency injection and containers from [wired](https://wired.readthedocs.io/en/latest/>), the components in your {doc}`pluggable apps <./pluggable>` are now swappable, easier to write and test, and less brittle.

:::{note}

  This is for people who want to make or consume a pluggable system.
  If that's not you, then it's unneeded complexity/magic.
:::

## Installation

For Python 3.7+:

```bash
$ pip install viewdom_wired
```

For Python 3.6, you'll need the `dataclasses` backport.

## Minimum Example

Register a component that will be used only in a certain circumstance:

```{literalinclude} ../examples/custom_context/site/components.py
---
start-after: Customizability
---
```


```{toctree}
---
hidden: true
---
who
what
why
pluggable
examples/index
future
```
