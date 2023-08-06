#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#
# pylint: disable=invalid-name

"""This files defines dataloader of THUCNews."""

import os

from ...dataset import Data, Dataset, DataType
from ...label import Classification, LabelType
from .._utility import glob

DATASET_NAME = "THUCNews"


def THUCNews(path: str) -> Dataset:
    """
    :param path: Path to THUCNews
    The folder structure should be like
    <path>
        <category>/
            0.txt
            1.txt
            2.txt
            3.txt
            ...
        <category>/
        ...
    :return: The loaded THUCNews dataset
    """
    root_path = os.path.abspath(os.path.expanduser(path))
    dataset = Dataset(DATASET_NAME, data_type=DataType.TEXT)
    dataset.load_label_tables(os.path.join(os.path.dirname(__file__), "labeltables.json"))
    segment = dataset.create_segment()

    categories = dataset.get_label_table(LabelType.CLASSIFICATION).categories
    for category in categories:
        text_paths = glob(os.path.join(root_path, category, "*.txt"))
        for text_path in text_paths:
            data = Data(text_path)
            data.append_label(Classification(category))

            segment.append(data)

    return dataset
