#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file contains healthcheck related functions."""

from typing import Callable, Generator, Generic, Iterable, List, TypeVar

_A = TypeVar("_A")
_R = TypeVar("_R")
ErrorGenerator = Generator[_R, None, None]
_Checker = Callable[[_A], ErrorGenerator[_R]]


class Pipeline(Generic[_A, _R]):
    """healthcheck pipeline to run registered checker functions"""

    def __init__(self) -> None:
        self._pipeline: List[_Checker[_A, _R]] = []

    def register(self, checker: _Checker[_A, _R]) -> _Checker[_A, _R]:
        """decorator function to register checkers into pipeline

        :param checker: the checker function needs to be registered
        :return: the checker function unchanged
        """
        self._pipeline.append(checker)
        return checker

    def __call__(self, args: _A) -> ErrorGenerator[_R]:
        for checker in self._pipeline:
            yield from checker(args)


class PipelineForIterable(Pipeline[_A, _R]):
    """healthcheck pipeline for processing iterable objects"""

    def __call__(self, args: Iterable[_A]) -> ErrorGenerator[_R]:  # type: ignore[override]
        for arg in args:
            yield from super().__call__(arg)
