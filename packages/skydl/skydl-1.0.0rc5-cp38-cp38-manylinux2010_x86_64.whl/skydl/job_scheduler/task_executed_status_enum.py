# -*- coding: utf-8 -*-
from enum import Enum, unique


@unique
class TaskExecutedStatusEnum(Enum):
    OK = 0
    FAIL = 1

    @staticmethod
    def from_id(id: int) -> Enum:
        for name, phase in TaskExecutedStatusEnum.__members__.items():
            if phase.value == id:
                return phase

    @staticmethod
    def get_id(enum_value: Enum) -> int:
        return enum_value.value
