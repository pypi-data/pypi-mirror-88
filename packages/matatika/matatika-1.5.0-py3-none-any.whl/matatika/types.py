"""types module"""

from enum import Enum


class Resource(Enum):
    """Matatika resource type enum"""

    WORKSPACE = 0
    DATASET = 1


class DataFormat(Enum):
    """Data format type enum"""

    RAW = 0
    CHARTJS = 1
