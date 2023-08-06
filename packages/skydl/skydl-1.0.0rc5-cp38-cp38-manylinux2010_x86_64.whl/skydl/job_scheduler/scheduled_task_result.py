# -*- coding: utf-8 -*-
from six import with_metaclass
from abc import ABCMeta, abstractmethod
from skydl.job_scheduler.task_executed_status_enum import TaskExecutedStatusEnum


class ScheduledTaskResult(with_metaclass(ABCMeta)):
    @property
    def task_executed_status_enum(self):
        return self._task_executed_status_enum

    @property
    def status_code(self):
        return self._status_code

    @property
    def msg(self):
        return self._msg

    @property
    def data(self):
        return self._data

    def __init__(self,
                 task_executed_status_enum: TaskExecutedStatusEnum = TaskExecutedStatusEnum.OK,
                 status_code: int = 0,
                 msg: str = "",
                 data: object = None):
        self._task_executed_status_enum = task_executed_status_enum
        self._status_code = status_code
        self._msg = msg
        self._data = data

    def with_success(self):
        return ScheduledTaskResult(TaskExecutedStatusEnum.OK, self.status_code, self.msg, self.data)

    def with_fail(self):
        return ScheduledTaskResult(TaskExecutedStatusEnum.FAIL, self.status_code, self.msg, self.data)

    def is_success(self):
        return self.task_executed_status_enum == TaskExecutedStatusEnum.OK

