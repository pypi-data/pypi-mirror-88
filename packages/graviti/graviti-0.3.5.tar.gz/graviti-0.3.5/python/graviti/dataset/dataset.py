#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class DatasetBase, Dataset and FusionDataset."""

import json
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, TypeVar, Union, overload

from typing_extensions import Literal

from ..label import AudioLabelTable, LabelTable, LabelTables, LabelType
from ..label.label_table import Tables
from ..utility import NameClass, NameSortedList, ReprType
from .segment import FusionSegment, Segment

T = TypeVar("T", FusionSegment, Segment)  # pylint: disable=invalid-name


class DataType(Enum):
    """this class defines the type of the data.

    :param data_type: The string of type of the data
    """

    IMAGE = "Image"
    POINT_CLOUD = "Point Cloud"
    AUDIO = "Audio"
    TEXT = "Text"
    OTHERS = "Others"


class DatasetBase(NameClass, Sequence[T]):
    """This class defines the concept of DatasetBase,
    which represents a whole dataset contains several segments.

    :param name: Name of the dataset
    :param is_continuous: Whether the data in dataset is continuous
    """

    _repr_type = ReprType.SEQUENCE

    def __init__(self, name: str, is_continuous: bool = False) -> None:
        super().__init__(name)
        self._segments: NameSortedList[T] = NameSortedList()
        self._label_tables: LabelTables = LabelTables()
        self._is_continuous = is_continuous

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[T]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[Sequence[T], T]:
        return self._segments.__getitem__(index)

    def __len__(self) -> int:
        return self._segments.__len__()

    @property
    def is_continuous(self) -> bool:
        """Check whether the data in dataset is continuous

        :return: Return `True` if the data is continuous, otherwise return `False`
        """
        return self._is_continuous

    @property
    def label_tables(self) -> LabelTables:
        """Return label tables

        :return: label tables
        """
        return self._label_tables

    def load_label_tables(self, loads: Union[Dict[str, Dict[str, Any]], str]) -> None:
        """Load label tables from json object.

        :param loads: LabelTables dict or the name of the file which contains the LabelTables dict
        """
        if isinstance(loads, str):
            with open(loads) as file:
                label_tables_dict = json.load(file)
        else:
            label_tables_dict = loads

        self._label_tables = LabelTables(loads=label_tables_dict)

    @overload
    def create_label_table(
        self,
        label_type: Literal[
            LabelType.CLASSIFICATION,
            LabelType.BOX2D,
            LabelType.BOX3D,
            LabelType.POLYGON2D,
            LabelType.POLYLINE2D,
        ],
    ) -> LabelTable:
        ...

    @overload
    def create_label_table(self, label_type: Literal[LabelType.SENTENCE]) -> AudioLabelTable:
        ...

    @overload
    def create_label_table(self, label_type: LabelType) -> Tables:
        ...

    def create_label_table(self, label_type: LabelType) -> Tables:
        """Create a new label table with given label type and add it to label tables.

        :param label_type: the label type of the label table to create

        :return: the created label table
        """

        return self._label_tables.create_label_table(label_type)

    @overload
    def get_label_table(
        self,
        label_type: Literal[
            LabelType.CLASSIFICATION,
            LabelType.BOX2D,
            LabelType.BOX3D,
            LabelType.POLYGON2D,
            LabelType.POLYLINE2D,
        ],
    ) -> LabelTable:
        ...

    @overload
    def get_label_table(self, label_type: Literal[LabelType.SENTENCE]) -> AudioLabelTable:
        ...

    @overload
    def get_label_table(self, label_type: LabelType) -> Tables:
        ...

    def get_label_table(self, label_type: LabelType) -> Tables:
        """return the label table corresponding to given LabeleType.

        :param label_type: a instance of LabelType
        :return: a label table
        """

        return self._label_tables[label_type]

    def get_label_types(self) -> Set[LabelType]:
        """return a set contains all label types.

        :return: a set of all label types
        """

        return set(self._label_tables.keys())

    def get_segment_by_name(self, name: str) -> T:
        """return the segment corresponding to given name.

        :param name: name of the segment
        :return: the segment which matches the input name
        """

        return self._segments.get_from_name(name)

    def add_segment(self, segment: T) -> None:
        """add segment to segment list.

        :param segment: a segment to be added
        """

        self._segments.add(segment)


class Dataset(DatasetBase[Segment]):
    """This class defines the concept of dataset,
    which contains a list of segments.

    :param name: Name of the dataset
    :param is_continuous: Whether the data in dataset is continuous
    :param data_type: Type of the data
    """

    def __init__(
        self, name: str, is_continuous: bool = False, data_type: Optional[DataType] = None
    ) -> None:
        super().__init__(name, is_continuous)
        self._data_type = data_type

    @property
    def data_type(self) -> Optional[DataType]:
        """Type of the data

        :return: Return type of the data
        """
        return self._data_type

    def create_segment(self, segment_name: str = "") -> Segment:
        """create a segment with the given name.

        :param segment_name: The name of the created segment
        :return: The created segment
        """
        segment = Segment(segment_name)
        self._segments.add(segment)
        return segment


class FusionDataset(DatasetBase[FusionSegment]):
    """This class defines the concept of multi-sensor dataset,
    which contains a list of multi-sensor segments.

    :param name: Name of the dataset
    :param is_continuous: Whether the data in dataset is continuous
    :param data_type: Type of the data
    """

    def __init__(
        self,
        name: str,
        is_continuous: bool = False,
        data_type: Union[Iterable[DataType], DataType, None] = None,
    ) -> None:
        super().__init__(name, is_continuous)
        self._data_type: List[DataType]
        if not isinstance(data_type, Iterable):  # pylint: disable=W1116
            self._data_type = [data_type] if data_type else []
        else:
            self._data_type = list(data_type)

    @property
    def data_type(self) -> List[DataType]:
        """Type of the data

        :return: Return type of the data
        """
        return self._data_type

    def create_segment(self, segment_name: str = "") -> FusionSegment:
        """create a fusion segment with the given name.

        :param segment_name: The name of the created fusion segment
        :return: The created fusion segment
        """
        segment = FusionSegment(segment_name)
        self._segments.add(segment)
        return segment
