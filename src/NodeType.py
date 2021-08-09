# -*- coding: utf-8 -*-
from enum import IntEnum

class NodeType(IntEnum):
    LITERAL = 1
    CLASS = 2
    URI = 3
    BLANK = 4
