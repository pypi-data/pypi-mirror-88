#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class MyRepr"""

from enum import Enum
from typing import Any, Callable, Dict, List, Mapping, Sequence, Tuple, Type, Union

ReprType = Enum("ReprType", ["HEAD", "INSTANCE", "SEQUENCE", "MAPPING"])


class ReprBase:  # pylint: disable=too-few-public-methods
    """repr base class to provide customized repr config and method"""

    _repr_type = ReprType.HEAD
    _repr_attributes: Tuple[str, ...] = ()
    _repr_maxlevel = 1

    def __str__(self) -> str:
        return _repr1(self, self._repr_maxlevel, self._repr_maxlevel, False)

    def __repr__(self) -> str:
        return _repr1(self, self._repr_maxlevel, self._repr_maxlevel, True)

    def _repr_head(self) -> str:
        return self.__class__.__name__


class _ReprConfig:  # pylint: disable=too-few-public-methods
    """config for customized repr method

    :param indent: the indent width for different level repr string
    :param maxlist: the max items displayed in the sequence repr string
    :param maxdict: the max items displayed in the mapping repr string
    """

    def __init__(self, indent: int = 2, maxlist: int = 16, maxdict: int = 16) -> None:
        self.indent = indent
        self.maxlist = maxlist
        self.maxdict = maxdict

    @property
    def indent(self) -> int:
        """
        The getter and setter of repr indent width

        :return: the indent width of repr config
        """
        return self._indent

    @indent.setter
    def indent(self, indent: int) -> None:
        self._indent = indent
        self._indent_str = " " * indent


repr_config = _ReprConfig()


class _ReprSequence(ReprBase, Sequence[Any]):  # pylint: disable=too-few-public-methods
    ...


class _ReprMapping(ReprBase, Mapping[Any, Any]):  # pylint: disable=too-few-public-methods
    ...


_ReprPrinter = Callable[[Any, int, int, bool], str]

_PRINTERS: Dict[Union[Type[Any], ReprType], _ReprPrinter] = {}


class _PrinterRegister:  # pylint: disable=too-few-public-methods
    """decorator class to register repr printer functions to `_PRINTERS`

    :param key: the key of the `_PRINTERS` for repr dispatch
    """

    def __init__(self, key: Union[Type[Any], ReprType]) -> None:
        self._key = key

    def __call__(self, printer: _ReprPrinter) -> _ReprPrinter:
        _PRINTERS[self._key] = printer
        return printer


def _repr1(obj: Any, level: int, maxlevel: int, folding: bool) -> str:
    """customized repr method

    :param obj: the object need to be transfer to repr string
    :param level: the current repr level
    :param maxlevel: the max repr level
    :return: "repr" of the object
    """
    repr_type = getattr(obj, "_repr_type", None)
    printer_key = repr_type if repr_type else type(obj)
    printer = _PRINTERS.get(printer_key, None)
    return printer(obj, level, maxlevel, folding) if printer else repr(obj)


@_PrinterRegister(ReprType.HEAD)
def _repr_head(obj: ReprBase, *_: Any) -> str:
    """customized repr method for `ReprType.HEAD`

    :param obj: the object need to be transfer to repr string
    :param level: the current repr level
    :param maxlevel: the max repr level
    :return: "repr" of the object
    """
    return obj._repr_head()  # pylint: disable=protected-access


@_PrinterRegister(ReprType.INSTANCE)
def _repr_instance(obj: ReprBase, level: int, maxlevel: int, folding: bool) -> str:
    """customized repr method for `ReprType.INSTANCE`

    :param obj: the object need to be transfer to repr string
    :param level: the current repr level
    :param maxlevel: the max repr level
    :return: "repr" of the object
    """
    # pylint: disable=protected-access
    if level <= 0:
        return f"{obj._repr_head()}(...)"

    newlevel = level - 1
    pieces: List[str] = []

    for attribute in obj._repr_attributes:
        value = getattr(obj, attribute, ...)
        if value is not ...:
            pieces.append(f"({attribute}): {_repr1(value, newlevel, maxlevel, folding)}")

    return f"{obj._repr_head()}{_join_with_indent(pieces, level, maxlevel, '(', ')')}"


@_PrinterRegister(ReprType.SEQUENCE)
def _repr_sequence(obj: _ReprSequence, level: int, maxlevel: int, folding: bool) -> str:
    """customized repr method for `ReprType.SEQUENCE`

    :param obj: the object need to be transfer to repr string
    :param level: the current repr level
    :param maxlevel: the max repr level
    :return: "repr" of the object
    """
    # pylint: disable=protected-access
    return f"{obj._repr_head()} {_repr_builtin_list(obj, level, maxlevel, folding)}"


@_PrinterRegister(ReprType.MAPPING)
def _repr_mapping(obj: _ReprMapping, level: int, maxlevel: int, folding: bool) -> str:
    """customized repr method for `ReprType.MAPPING`

    :param obj: the object need to be transfer to repr string
    :param level: the current repr level
    :param maxlevel: the max repr level
    :return: "repr" of the object
    """
    # pylint: disable=protected-access
    return f"{obj._repr_head()} {_repr_builtin_dict(obj, level, maxlevel, folding)}"


@_PrinterRegister(list)
def _repr_builtin_list(obj: Sequence[Any], level: int, maxlevel: int, folding: bool) -> str:
    """customized repr method for buildin type `list`

    :param obj: the object need to be transfer to repr string
    :param level: the current repr level
    :param maxlevel: the max repr level
    :return: "repr" of the object
    """
    return _repr_builtin_sequence(obj, level, maxlevel, folding, "[", "]")


@_PrinterRegister(tuple)
def _repr_builtin_tuple(obj: Sequence[Any], level: int, maxlevel: int, folding: bool) -> str:
    """customized repr method for buildin type `tuple`

    :param obj: the object need to be transfer to repr string
    :param level: the current repr level
    :param maxlevel: the max repr level
    :return: "repr" of the object
    """
    return _repr_builtin_sequence(obj, level, maxlevel, folding, "(", ")")


@_PrinterRegister(dict)
def _repr_builtin_dict(obj: Mapping[Any, Any], level: int, maxlevel: int, folding: bool) -> str:
    """customized repr method for buildin type `dict`

    :param obj: the object need to be transfer to repr string
    :param level: the current repr level
    :param maxlevel: the max repr level
    :return: "repr" of the object
    """
    object_length = len(obj)
    if object_length == 0:
        return "{}"
    if level <= 0:
        return "{...}"
    newlevel = level - 1
    try:
        keys = sorted(obj)
    except Exception:  # pylint: disable=broad-except
        keys = list(obj)

    fold, unfold = _calculate_fold_number(object_length, repr_config.maxdict, folding)
    pieces = [
        f"{repr(key)}: {_repr1(obj[key], newlevel, maxlevel, folding)}" for key in keys[:unfold]
    ]
    if fold:
        key = keys[-1]
        pieces.append(f"... ({fold} items are folded)")
        pieces.append(f"{repr(key)}: {_repr1(obj[key], newlevel, maxlevel, folding)}")

    return _join_with_indent(pieces, level, maxlevel, "{", "}")


def _repr_builtin_sequence(  # pylint: disable=too-many-arguments
    obj: Sequence[Any], level: int, maxlevel: int, folding: bool, left: str, right: str
) -> str:
    """customized repr method for sequence

    :param obj: the object need to be transfer to repr string
    :param level: the current repr level
    :param maxlevel: the max repr level
    :param left: the left bracket symbol
    :param right: the right bracket symbol
    :return: "repr" of the object
    """
    object_length = len(obj)
    if object_length == 0:
        return f"{left}{right}"
    if level <= 0:
        return f"{left}...{right}"
    newlevel = level - 1

    fold, unfold = _calculate_fold_number(object_length, repr_config.maxlist, folding)
    pieces = [_repr1(item, newlevel, maxlevel, folding) for item in obj[:unfold]]
    if fold:
        pieces.append(f"... ({fold} items are folded)")
        pieces.append(_repr1(obj[-1], newlevel, maxlevel, folding))

    return _join_with_indent(pieces, level, maxlevel, left, right)


def _calculate_fold_number(length: int, max_length: int, folding: bool) -> Tuple[int, int]:
    """calculate the number of the folded and unfolded items

    :param length: the object length
    :param max_length: the configured max length
    :return: the number of the folded items & the number of the unfolded items
    """
    if folding and length > max_length:
        return length - max_length + 1, max_length - 2
    return 0, length


def _join_with_indent(pieces: List[str], level: int, maxlevel: int, left: str, right: str) -> str:
    """handle the indent, newline and "," of the string list

    :param pieces: the string list need to be transfer to repr string
    :param level: the current repr level
    :param maxlevel: the max repr level
    :param left: the left bracket symbol
    :param right: the right bracket symbol
    :return: repr string with indent, newline and ","
    """
    # pylint: disable=protected-access
    inner_indent = repr_config._indent_str * (maxlevel - level + 1)
    outer_indent = repr_config._indent_str * (maxlevel - level)

    sep = f",\n{inner_indent}"
    return f"{left}\n{inner_indent}{sep.join(pieces)}\n{outer_indent}{right}"
