import abc
from typing import Set, Type, TypeVar

T = TypeVar('T')


def get_subclasses(cls: Type[T]) -> Set[Type[T]]:
    # Get subclasses of task, which not abstract
    # https://pydantic-docs.helpmanual.io/usage/models/#abstract-base-classes

    subclasses = set()
    for sc in cls.__subclasses__():
        # Skip if last MRO base is ABC
        if abc.ABC != sc.__mro__[1]:
            subclasses.add(sc)

        subclasses.update(get_subclasses(sc))

    return subclasses
