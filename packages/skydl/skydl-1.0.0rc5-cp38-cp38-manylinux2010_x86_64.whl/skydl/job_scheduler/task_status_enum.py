# -*- coding: utf-8 -*-
from enum import Enum, unique


@unique
class TaskStatusEnum(Enum):
    READY = 0       # 人工可以设置的最终状态
    RUNNING = 1     # 程序设置的中间状态
    FINISHED = 2    # 程序设置的中间状态
    KILLED = 3      # 程序设置的中间状态
    FAILED = 4      # 程序设置的中间状态
    SKIPPED = 5     # 人工可以设置的最终状态

    @staticmethod
    def from_id(id: int) -> Enum:
        for name, phase in TaskStatusEnum.__members__.items():
            if phase.value == id:
                return phase

    @staticmethod
    def get_id(enum_value: Enum) -> int:
        return enum_value.value
