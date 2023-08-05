# Why It Is Useful

Yes, this approach is different from the status-quo approach of convention-over-configuration, with magic names and magic strings.
It is explicit instead of implicit, which is more work, more boilerplate, and some admittedly-magical-voodoo in the middle.
What makes it worth it?

Let's take a look (although some of this includes benefits from `viewdom`, `htm.py`, and `tagged`.)

## Pythonic

Modern Python template engines come from a time when splitting out the "HTML Designer" was a primary goal.
Give them an artifact that felt like HTML, with some special operations, and keep them safe from the Python.
(Implicitly: keep us safe from them.)

Thus, templates gaines a parallel universe with lots of constructs in Python, but...different.

My assertion: most hours spent today in front of Jinja2 are by Python developers doing HTML, not vice versa.
For this audience, it would be nice to use:

- Actual Python expressions, looping, conditionals, etc.

- Python organization concepts such as packages, symbol imports, scopes

- Quality control tools such as unit testing, linters, mypy, refactoring, IDEs

In fact, one could argue that "templates" need these quality control tools at least as much as Python code.

## Explicit vs. Implicit

In modern templating, scope is unbelievably magical.
If you're looking at pixels from a Sphinx document, trying to find what rendered that `<div>` is one heck of an adventure.
Same is true for Django, Flask, even Go templates in Hugo.
In the name of "convenience", they provide a garbage barge of scope.

This is equally true when looking at the units of organization.
What is needed inside a macro?
If something changes in that macro, how will I know if callers are broken?
Where does a parent template come from and what "contract" does it provide?

In the world of React components and things like JSX/htm, the language is used to glue things together.
With the addition of TypeScript, components more formally explain what they provide/require.

Python believes in "Explicity is better than implicit" but Python templating seems to take a different approach.
With the advent of type hinting, Python templating has an opportunity to have a more formal, reliable, software-development approach to components and UIs.

Obviously some hate type hinting and prefer conventions.

## Static Analysis

What if your CI could warn you about a missing prop when using a component?
What if your editor could give you a red squiggly in a template?

If you're trying to do a pluggable system, with different actors creating and consuming things, you want to know if the rules are being followed.
In Python, that means testability (below.)
But what if you could "fail faster", before running or even writing tests?

When writing React components and using TypeScript, the TypeScript compiler looks at TSX and yells when a component's contract is violated.
Inside the component, the compiler yells when you use something from the scope incorrectly.
The rules are enforced and reported real-time.

This is a tremendous help for large, loosely-coupled ecosystems such as Sphinx, where everybody is kind of at arms-length.
It would be a boon to Sphinx if an add-on could run `mypy` and know that its templates were ok.

`viewdom_wired`, for better or worse, embraces this.
Components are written as single-callable dataclasses.
The only things in scope are things in the dataclass.

## Extensibility

In Python, the first step of pluggability is extensability.
Meaning, I want to add a new thing, something with no connection to an existing thing.
A new template filter, for example.

This is the primary unit of pluggability for a number of Python web systems.
But even for this simple first step, it frequently involves magic: "Put a special filename in a special directory and we'll look for a special function and pass some specially named arguments."
Many view this approach -- convention over configuration -- as a positive, but it has some downsides.

## Replaceability

Here's a next level of pluggability: registering something that replaces a built-in capability.
"Instead of the built-in Image implementation, use this one instead."
This is actually a rare thing.

## Customizability

As a third level of pluggability, perhaps you want the built-in `Image` in some cases, but a custom `Image` in others.
This is pretty hard, because it requires a fork of all the callers of `Image`.

Pyramid does a great job at this.
You can register a `view` for many different conditions, called `predicates`.
You can even (with enough work) create your own kinds of things, not just `views` and not just the built-in `predicates`.

Why is this useful?
A site can adapt to its peculiar uses without forking.
And with dependency injection, it can gather extra information from the environment, without requiring the callers to pass in new arguments (which also would mean forking.)

## Single Responsibility Principle

Within 3 commits, most templates become a soup of conditional branches, loops, scope-defeating variable overrides, and the like.
What started as separation of concerns becomes multiply concerning.

In modern frontends, the move has been towards the `single responsibility principle <https://en.wikipedia.org/wiki/Single-responsibility_principle>`_.
Lots and lots of small, testable units of rendering.
Sometimes the state and logic are moved to "container components" which push templating into smaller, child "presentation components".

`viewdom_wired` tries to enable this pattern.
Units are self-contained in logic and scope, then explicitly (via import) combined into parent components.

## Testability

How would you unit test a template?
It almost makes no sense.
The scope comes from...who knows.
If it calls macros, you're no longer in Python, so you have to assemble a template environment from the application which finds all the magical macro locations.

`viewdom_wired` makes a component dead-simple to render.
You pass values into a dataclass then call its `__html__` method.
You don't really even need to assemble an injector, as in theory, that's a DSL that the host environment manages testing for.

## SSR/CSR

Here's one odd aspect to this approach: the same template can (somewhat) render server-side in Python and browser-side.

The first, easiest way is through the layers involved in this approach.
`viewdom.html` generates a VDOM, then passed to `viewdom_wired.render` for conversion to a string.
One could skip the second step and send the browser the VDOM, which could be used to React/Preact/Vue etc. to update a block in the browser.
This has quite a number of the benefits from "modern web."

There's a step beyond this, albeit very experimental.
One could use `Transcrypt <http://www.transcrypt.org>`_ to convert the component dataclass to a JavaScript module.
This would then re-render without a trip to the server.
With something like this, you would get what's currently considered best practice:

- Server-side rendering (SSR) for initial load, for SEO indexing, and for non-JavaScript clients

- Client-side rendering (CSR) via rehydration for subsequent updates after the first load

A proof-of-concept was done for this with `htm.py`.
