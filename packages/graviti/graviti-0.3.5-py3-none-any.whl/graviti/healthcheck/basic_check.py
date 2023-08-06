#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file contains basic healthcheck functions."""


from typing import Union

from ..dataset import Dataset, FusionDataset
from .pipeline import ErrorGenerator
from .report import Error


class BasicError(Error):  # pylint: disable=too-few-public-methods
    """The base class of the basic error

    :param name: the dataset or segment name which has error
    """

    def __init__(self, name: str) -> None:
        self._name = name


class EmptyDatasetError(BasicError):  # pylint: disable=too-few-public-methods
    """the error class for empty dataset"""

    def __str__(self) -> str:
        return f"Dataset '{self._name}' is empty"


class EmptySegmentError(BasicError):  # pylint: disable=too-few-public-methods
    """the error class for empty segment"""

    def __str__(self) -> str:
        return f"Segment '{self._name}' is empty"


def check_basic(dataset: Union[Dataset, FusionDataset]) -> ErrorGenerator[BasicError]:
    """the health check function for basic

    :param dataset: the `Dataset` or `FusionDataset` object needs to be checked
    :return: a generator of `BasicError`
    """

    if not dataset:
        yield EmptyDatasetError(dataset.name)
        return

    for segment in dataset:
        if not segment:
            yield EmptySegmentError(segment.name)
