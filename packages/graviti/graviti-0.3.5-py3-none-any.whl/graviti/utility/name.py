#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class NameClass"""

from collections import OrderedDict
from typing import Dict, Iterator, List, Mapping, Optional, Sequence, TypeVar, Union, overload

from sortedcontainers import SortedDict

from .repr import ReprBase
from .user import UserMapping


class NameClass(ReprBase):
    """A mixin class for instance which has immutable name and mutable description

    :param name: A string representing the class name
    :param loads: A dict contains name and description
    :raises
        TypeError: Name required when not given loads
    """

    def __init__(
        self,
        name: Optional[str] = None,
        *,
        loads: Optional[Dict[str, str]] = None,
    ) -> None:
        if loads:
            self._name = loads["name"]
            self.description = loads.get("description", "")
            return

        if name is None:
            raise TypeError(
                f"{self.__class__.__name__}() missing 1 required positional argument: 'name'."
            )

        self._name = name
        self.description = ""

    def _repr_head(self) -> str:
        return f'{self.__class__.__name__}("{self._name}")'

    def dumps(self) -> Dict[str, str]:
        """Dumps the instance as a dictionary.

        :return: A dictionary containing name and description
        """
        data = {"name": self._name}
        if self.description:
            data["description"] = self.description

        return data

    @property
    def name(self) -> str:
        """Return name of the instance.

        :return: Name of the instance
        """
        return self._name


T = TypeVar("T", bound=NameClass)  # pylint: disable=invalid-name


class NameSortedDict(UserMapping[str, T]):
    """Name sorted dict is a sorted mapping which contains `NameClass`,
    the corrsponding key is the 'name' of `NameClass`.
    Name sorted dict keys are maintained in sorted order.

    :param data: A mapping from str to `NameClass` which needs to be transferred to `NameSortedDict`
    """

    def __init__(self, data: Optional[Mapping[str, T]] = None) -> None:
        self._data: SortedDict = SortedDict(data)

    def add(self, value: T) -> None:
        """Store item in name sorted dict"""
        self._data[value.name] = value


class NameSortedList(Sequence[T]):
    """Name sorted list is a sorted sequence which contains `NameClass`,
    Name sorted list are maintained in sorted order according to the name of NameClass.
    """

    def __init__(self) -> None:
        self._data = SortedDict()

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> List[T]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[T, List[T]]:
        return self._data.values()[index]  # type: ignore[no-any-return]

    def __len__(self) -> int:
        return self._data.__len__()  # type: ignore[no-any-return]

    def __iter__(self) -> Iterator[T]:
        return self._data.values().__iter__()  # type: ignore[no-any-return]

    def add(self, value: T) -> None:
        """Store item in name sorted list."""
        self._data[value.name] = value

    def get_from_name(self, name: str) -> T:
        """Get item in name sorted list from name of NameClass."""
        return self._data[name]  # type: ignore[no-any-return]


class NameOrderedDict(UserMapping[str, T]):
    """Name ordered dict is an ordered mapping which contains `NameClass`,
    the corrsponding key is the 'name' of `NameClass`.
    Name sorted dict keys are maintained in sorted order.

    :param data: A mapping from str to `NameClass`
                which needs to be transferred to `NameOrderedDict`
    """

    def __init__(self) -> None:
        self._data: "OrderedDict[str, T]" = OrderedDict()

    def append(self, value: T) -> None:
        """Store item in ordered dict."""
        self._data[value.name] = value
