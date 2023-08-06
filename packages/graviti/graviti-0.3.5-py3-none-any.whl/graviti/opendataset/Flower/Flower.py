#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#
# pylint: disable=invalid-name

"""This file defines the 17 Category Flower and 102 Category Flower Dataloaders"""

import os

from ...dataset import Data, Dataset
from ...label import Classification, LabelType
from .._utility import glob

DATASET_NAME_17 = "Flower17"
DATASET_NAME_102 = "Flower102"


def Flower17(path: str) -> Dataset:
    """Load the 17 Category Flower Dataset to TensorBay

    :param path: the root directory of the dataset
    The file structure should be like:
    <path>
        jpg/
            image_0001.jpg
            ...

    :return: a loaded dataset
    """
    root_path = os.path.abspath(os.path.expanduser(path))

    image_paths = glob(os.path.join(root_path, "jpg", "*.jpg"))

    dataset = Dataset(DATASET_NAME_17)
    dataset.load_label_tables(os.path.join(os.path.dirname(__file__), "labeltables_17.json"))
    categories = list(dataset.label_tables[LabelType.CLASSIFICATION].categories)
    segment = dataset.create_segment()

    for image_path in image_paths:
        data = Data(os.path.join(root_path, image_path))
        data.register_label(LabelType.CLASSIFICATION)

        # There are 80 images for each category
        index = int(image_path[6:10]) - 1
        data.append_label(Classification(category=categories[index // 80]))
        segment.append(data)

    return dataset


def Flower102(path: str) -> Dataset:
    """Load the 102 Category Flower Dataset to TensorBay

    :param path: the root directory of the dataset
    The file structure should be like:
    <path>
        jpg/
            image_00001.jpg
            ...
        imagelabels.mat
    :return: a loaded dataset
    """
    from scipy.io import loadmat  # pylint: disable=import-outside-toplevel

    root_path = os.path.abspath(os.path.expanduser(path))
    image_paths = glob(os.path.join(root_path, "jpg", "*.jpg"))
    labels = loadmat(os.path.join(root_path, "imagelabels.mat"))["labels"][0]

    dataset = Dataset(DATASET_NAME_102)
    dataset.load_label_tables(os.path.join(os.path.dirname(__file__), "labeltables_102.json"))
    categories = list(dataset.label_tables[LabelType.CLASSIFICATION].categories)
    segment = dataset.create_segment()
    for image_path in image_paths:
        index = int(os.path.basename(image_path)[6:11]) - 1
        data = Data(image_path)
        data.append_label(Classification(categories[int(labels[index]) - 1]))
        segment.append(data)
    return dataset
