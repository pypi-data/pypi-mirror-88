# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Callable
from six import with_metaclass
from abc import ABCMeta, abstractmethod
import traceback
from skydl.common.date_utils import DateUtils
from skydl.job_scheduler.scheduled_task_result import ScheduledTaskResult
from skydl.job_scheduler.task_status_enum import TaskStatusEnum


def default_scheduled_callable_func():
    return ScheduledTaskResult()


class ScheduledTask(with_metaclass(ABCMeta)):
    """
    可执行的任务对象
    :param unique_name 任务名称，必须全局唯一 e.g. "hk_foo_task", "us_foo_task"
    :param desc 任务简单描述
    :param ordered 序号，可用于排序
    :param status 运行结果状态
    :param start_time  任务开始时间
    :param end_time  任务结束时间
    :param callable 可运行的任务内容 可以用SimpleSparkJobScheduler.implicitCallableFunc  e.g. callable = new Callable[Object] { def call(): ScheduledTaskResult { ScheduledTaskResult() } }
    :param run_info 运行时的一些结果信息
    """
    @property
    def unique_name(self):
        return self._unique_name

    @property
    def desc(self):
        return self._desc

    @property
    def ordered(self):
        return self._ordered

    @property
    def status(self):
        return self._status

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def callable(self):
        return self._callable

    @property
    def run_info(self):
        return self._run_info

    def __init__(self,
                 unique_name: str = "foo_task",
                 desc: str = "",
                 ordered: int = 0,
                 status: TaskStatusEnum = TaskStatusEnum.READY,
                 start_time: datetime = None,
                 end_time: datetime = None,
                 callable: Callable[[], ScheduledTaskResult] = default_scheduled_callable_func,
                 run_info: str = ""):
        self._unique_name = unique_name
        self._desc = desc
        self._ordered = ordered
        self._status = status
        self._start_time = start_time
        self._end_time = end_time
        self._callable = callable
        self._run_info = run_info

    def call(self):
        self._status = TaskStatusEnum.RUNNING
        self._start_time = DateUtils.now()
        try:
            self.callable()
            self.finish()
        except Exception as e:
            self.fail("exception occured on scheduler task[" + self.unique_name + "]: " + str(e))
            print("exception occured on scheduler task[" + self.unique_name + "]: " + str(e))
            traceback.print_exc()

    def kill(self, kill_msg: str = ""):
        self._status = TaskStatusEnum.KILLED
        self._end_time = DateUtils.now()
        self._run_info = kill_msg
        return self

    def fail(self, error_msg: str = ""):
        self._status = TaskStatusEnum.FAILED
        self._end_time = DateUtils.now()
        self._run_info = error_msg
        return self

    def finish(self):
        self._status = TaskStatusEnum.FINISHED
        self._end_time = DateUtils.now()
        return self

    def skip(self):
        self._status = TaskStatusEnum.SKIPPED
        self._end_time = DateUtils.now()
        return self