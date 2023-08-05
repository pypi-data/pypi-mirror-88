# Classes

Let's write a basic application using the pluggability ideas in `viewdom_wired`.
We'll start with something very basic and gradually introduce some of the basic ideas.
All of these examples are in the repository's `examples` directory with tests that cover them in the `tests` directory.

## hello_world

The simplest possible example:
A single function which recreates the universe whenever it is run:

```{literalinclude} ../../examples/hello_world/app.py
---
start-after: from viewdom_wired
---
```

## hello_children

Same example, but the injector respects the special flag of children, to allow the component to be passed in some contained nodes.

```{literalinclude} ../../examples/hello_children/app.py
---
start-after: from viewdom_wired
---
```

In this example, the template uses `Greeting` and passes a span.
The component says it accepts children and provides a default template to use if none are provided.
If this component's doesn't use `children`, it should simply delete the field, but it can also provide a default value of an empty tuple `()`.

## hello_app

Of course that's not very real-world.
Let's show a case that splits the three roles.

First, a pluggable app:

```{literalinclude} ../../examples/hello_app/app.py
---
start-after: from wired_injector
---
```

Then, a third-party plugin for the app, providing a component that can be used in a site:

```{literalinclude} ../../examples/hello_app/plugin.py
---
start-after: from viewdom
---
```

Finally, the site itself, which uses the app and the third-party plugin to render a response:

```{literalinclude} ../../examples/hello_app/site.py
---
start-after: from viewdom_wired
---
```

## app_plugin_site

Let's re-organize the layout to emphasize the 3 roles: *app*, *plugins*, and a *site*.

The app, which stores the registry:

```{literalinclude} ../../examples/app_plugin_site/site/__init__.py
---
start-after: from viewdom_wired
---
```

A `greeting` plugin with a component and a `wired_setup` function to set itself up:

```{literalinclude} ../../examples/app_plugin_site/plugins/greeting/__init__.py
---
start-after: from wired_injector
---
```

And finally a site that uses the pluggable app and the plugin:

```{literalinclude} ../../examples/app_plugin_site/site/__init__.py
---
start-after: from viewdom
---
```


## app_decorators_render

We now switch to an app which can register decorator-based plugins, passing them the registry for self-configuration.

The pluggable app is richer, including a `venusian` decorator scanner.
You can now tell the app to setup a plugin module:

```{literalinclude} ../../examples/app_decorators_render/site/__init__.py
---
start-at: def site_startup
---
```

The plugin's `wired_setup` can now register itself, getting passed the app instance:

```{literalinclude} ../../examples/app_decorators_render/plugins/greeting/__init__.py
---
start-at: from . import greeting
---
```

The plugin has a component:

```{literalinclude} ../../examples/app_decorators_render/plugins/greeting/greeting.py
---
start-at: from wired_injector
---
```

This time, the site has a "view" which handles the response.
It uses the plugin's `Greeting` component:

```{literalinclude} ../../examples/app_decorators_render/site/views.py
---
start-after: from viewdom
---
```

## override

Now we get into the strength of `viewdom_wired`: a registration which *replaces* component from another package.

Nothing changes in the pluggable app nor in the plugins.
The site is in control: it can register replacements.

Here is the site, which now scans for local components which might add to *or replace* components:

```{literalinclude} ../../examples/override/site/__init__.py
---
start-at: from . import components
---
```

The site now has a components file:

```{literalinclude} ../../examples/override/site/components.py
---
start-at: injectable(for_=Greeting)
---
```

The site's `views.py` remains the same.
When its template asks for a `Greeting` component, a different implementation is provided.

```{literalinclude} ../../examples/override/site/views.py
---
start-after: from viewdom
---
```

One thing that is nice about this: we didn't use subclassing to establish the is-a relationship between `Greeting` and `SiteGreeting`.
Instead, the registration handled this with the `for_`.

## context

Components don't have to get all their info from passed-in props.
They can ask the injector to get information for them, for example, from the `wired` container's context.

The app changes, as ``render`` now accepts a context, which it puts in the container:

```{literalinclude} ../../examples/context/app/__init__.py
---
start-after: from viewdom_wired
---
```

Here's a **big** point: the component asks the *injector* to get the *context*.
Thus, the parent components don't have to pass this all the way down.
Moreover, the injector is asked to get a specific attribute off the context, which is nice for two reasons:

- The consumer of this component could pass in a different value, superseding the injector value

- The component has a smaller surface area with the outside world, instead of getting the entire context

```{literalinclude} ../../examples/context/plugins/greeting/greeting.py
---
start-after: from viewdom
---
```

The site defines different kinds of contexts:

```{literalinclude} ../../examples/context/site/contexts.py
---
start-after: from dataclasses
---
```

The site then makes a context to use during rendering:

```{literalinclude} ../../examples/context/site/__init__.py
---
start-at: from .contexts
---
```

Of course in a bigger system, the pluggable app might handle creating the context, e.g. by looking at the incoming URL.

## custom_context

Another benefit: different flavors of component based on the "context".
The app can render using a container that has a context value.
The plugin can then provide a component for the default and a different implementation for a certain context.

We now have two kinds of context:

```{literalinclude} ../../examples/custom_context/site/contexts.py
---
start-after: from dataclasses
---
```

The site then makes a local flavor of the `Greeter` component, for use with the new kind of context:

```{literalinclude} ../../examples/custom_context/site/components.py
---
start-after: from wired_injector
---
```

The template in the view doesn't have to change.
Any other components that use a `Greeting` component, don't have to change.
They just get a `FrenchGreeting` in appropriate cases.
