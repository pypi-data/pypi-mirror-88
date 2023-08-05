# Interfaces

In [](./classes) we saw how to provide different flavors of components, using `for_` to establish the relationship.
This solves the registration problem, but other parts of your code don't know that `SiteGreeter` is a kind of `Greeter`.

While we could use subclassing, sharing the implementation has downsides.
