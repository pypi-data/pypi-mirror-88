#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file contains healthcheck related functions."""


from collections import OrderedDict
from typing import Any, Callable, List, TypeVar

from ..label import LabelType
from ..utility import UserMutableMapping, UserSequence


class Error:  # pylint: disable=too-few-public-methods
    """Base class of healthcheck errors"""

    def __str__(self) -> str:
        ...


class _ErrorContext:
    _S = TypeVar("_S", bound="_ErrorContext")

    def __init__(self, title: str) -> None:
        self._title = title

    def __enter__(self: _S) -> _S:
        print("-------------------------------------------")
        print(self._title)
        return self

    def __exit__(self, *_: Any) -> None:
        if not self:
            print("PASS")


class _ErrorSection(UserSequence[Error]):
    def __init__(self) -> None:
        self._data: List[Error] = []

    def append(self, error: Error) -> None:
        """Append a error to the end of the error list

        :param error: the error object needs to be appended
        """
        self._data.append(error)
        print(f"    {error}")


class _ErrorList(_ErrorSection, _ErrorContext):
    def __init__(self, title: str) -> None:
        _ErrorSection.__init__(self)
        _ErrorContext.__init__(self, title)

    def append(self, error: Error) -> None:
        """Append a error to the end of the error list

        :param error: the error object needs to be appended
        """
        if not self:
            print("FAILED")

        self._data.append(error)
        print(f"  {error}")


_T = TypeVar("_T")


class _ErrorDict(UserMutableMapping[_T, _ErrorSection], _ErrorContext):
    def __init__(self, title: str, key_printer: Callable[[_T], str] = str) -> None:
        _ErrorContext.__init__(self, title)
        self._data = OrderedDict()
        self._key_printer = key_printer

    def __getitem__(self, key: _T) -> _ErrorSection:
        try:
            return self._data.__getitem__(key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key: _T) -> _ErrorSection:
        if not self:
            print("FAILED")
        print(f"  {self._key_printer(key)}:")
        value = _ErrorSection()
        self._data.__setitem__(key, value)
        return value


class HealthReport:  # pylint: disable=too-few-public-methods
    """the result of the healthcheck, which contains all the errors"""

    def __init__(self) -> None:
        self.basic_reports = _ErrorList("Basic checking:")
        self.label_table_reports: _ErrorDict[LabelType] = _ErrorDict(
            "LableTable checking:", lambda key: key.name
        )
