# Who This Is For

There's a certain pattern where different roles/parties collaborate in an ecosystem.
I'm labeling this a {doc}`pluggable app <./pluggable>`.

For example, Sphinx is a pluggable app.
Sphinx might ship a directive for rendering an image.
Some ``modern-sphinx`` theme might have a different take on images, making them responsive with placeholders.
Then, some site that uses ``Sphinx`` with the ``modern-sphinx`` theme might want, in some limited situation, a different kind of image.
Three roles, working together to produce a custom site.

[Material-UI](https://material-ui.com>) is another example.
It's a ready-to-go, attractive component system for React, based on Material Design.
But even though React has a more formal idea of "component" than Sphinx, and even though Material-UI has learned a lot over the years about boundaries, it's a hard trick to pull off.
Consumers want something read-to-go, something with rules, but always ask for exceptions to the rules.

`viewdom_wired` is for people who want a broad system, with clear boundaries, that's highly customizable, but in a sane way.
Too often, Python system optimize for the goal of "Super Easy First Five Minutes".
Alas, this tends to lead to a miserable next five years, when the magic breaks down.

If you're willing to trade a bit of first-contact convenience for something that scales, then "pluggable apps" might be a good fit for you.
