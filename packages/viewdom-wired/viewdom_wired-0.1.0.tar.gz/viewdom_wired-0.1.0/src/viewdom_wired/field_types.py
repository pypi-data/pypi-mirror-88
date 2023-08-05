"""

Dataclass field helpers.
"""

from dataclasses import field, Field
from typing import TypeVar

T = TypeVar('T')


def injected(type_, *args, **kwargs) -> Field:
    """Get a value from an injected type

    We frequently want part of an injectable or adapter. Just an attribute
    or, for injectable/adapters that are dict-like, a key.

    This field type accepts an injectable/adapter and serves three purposes:

    - Get an attribute off of it by passing in attr='somevalue'

    - Or, get a key out of it by passing in key=''

    - Or, if the injectable/adapter has a __call__, return the value
      of calling it

    - Otherwise, return the injectable/adapter, same as if you didn't
      provide a field

     We could just manually do ``injected`` then pick apart the injected
     value. But that exposes a big surface area. This field type lets us
     zero in on what we want.
    """

    # If metadata was also passed in, preserve it, otherwise start clean
    if 'metadata' not in kwargs:
        kwargs['metadata'] = {}

    kwm = kwargs['metadata']
    kwm['injected'] = dict(type_=type_, pipeline=args)

    return field(**kwargs)
