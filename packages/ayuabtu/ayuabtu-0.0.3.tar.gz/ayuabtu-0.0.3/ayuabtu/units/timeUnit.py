# Author: Lukas Halbritter <halbritl@informatik.uni-freiburg.de>
# Copyright 2020
from enum import Enum


class TimeUnit(Enum):
    WEEK = 1
    DAY = 2
    HOUR = 3
    MINUTE = 4
    SECOND = 5
    MILLISECOND = 6
    MICROSECOND = 7
    NANOSECOND = 8
