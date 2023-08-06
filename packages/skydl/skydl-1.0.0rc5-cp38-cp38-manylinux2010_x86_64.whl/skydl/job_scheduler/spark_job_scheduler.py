# -*- coding: utf-8 -*-
from datetime import datetime
from six import with_metaclass
from abc import ABCMeta, abstractmethod
from skydl.common.date_utils import DateUtils
from skydl.common.enhanced_ordered_dict import EnhancedOrderedDict
from skydl.job_scheduler.task_status_enum import TaskStatusEnum
from skydl.job_scheduler.scheduled_task_result import ScheduledTaskResult
from skydl.job_scheduler.scheduled_task import ScheduledTask, default_scheduled_callable_func


class SparkJobScheduler(with_metaclass(ABCMeta)):
    """
    任务Pipeline：一个主任务可以按顺序任意组合调用下面的子任务，主任务执行完后可以接着调用下一个主任务
    同步任务串行执行的job scheduler, 有checkpoint机制，重启后可以接着上次正在处理的job继续运行
    配置覆盖的优先顺序：代码定义的task -> initFromCheckpoint(只恢复FINISHED,FAILED,RUNNING,KILLED的状态，不恢复READY,SKIP的状态) -> skipTaskNameMap(只SKIP掉值为true的task)
    :param uniqueName job调度器名称，必须全局唯一 e.g. "hk_spark_job_scheduler_batch"
    :param desc job调度器描述
    :param checkpointPath checkpoint路径
    :param initFromCheckpoint 是否从checkpoint初始化状态
    :param skipTaskNameMap 应被忽略执行的任务名称map, e.g. {"foo_task":true,"bar_task":false}
    usage:
    ......
    val skipTaskNameMap: java.util.HashMap[String, Boolean] = new java.util.HashMap()
    skipTaskNameMap.put("foo1", true)
    skipTaskNameMap.put("foo3", false)
    val scheduler = new SparkJobScheduler("sampleScheduler", desc="Spark简单调度器例子", initFromCheckpoint=true, checkpointPath=checkpointPath, skipTaskNameMap=skipTaskNameMap)
    import scheduler.implicitRunnableFunc
    scheduler.schedule(ScheduledTask("foo1", "第一个任务", 1, TaskStatusEnum.READY, runnable=()=>{
      foo(spark)
    }))
    .schedule(ScheduledTask("foo2", "第二个任务", 2, TaskStatusEnum.READY, runnable=()=>{
      log.info("xxxxxxx")
    }))
    .schedule(ScheduledTask("foo3", "第三个任务", 3, TaskStatusEnum.SKIP, runnable=()=>{
      val i = 1/0
      log.info("yyyyyyy")
    }))
    .schedule(ScheduledTask("foo4", "第四个任务", 4, TaskStatusEnum.READY, runnable=()=>{
      log.info("zzzzz")
    }))
    .process()
    ......
  未来路线需实现的功能列表：
  1.DAG 可以参考spark的DAG实现，python的networkx, 和scala的实现：https://github.com/stripe/dagon
  2.处理故障策略(已经引进failsafe)：https://github.com/jhalterman/failsafe
  3.可视化配置参数及job监控后台
    """
    @property
    def unique_name(self):
        return self._unique_name

    @property
    def desc(self):
        return self._desc

    @property
    def init_from_checkpoint(self):
        return self._init_from_checkpoint

    @property
    def checkpoint_path(self):
        return self._checkpoint_path

    @property
    def skip_task_name_map(self):
        return self._skip_task_name_map

    @property
    def task_list(self):
        return self._task_list

    def __init__(self,
                 unique_name: str = "SparkJobScheduler",
                 desc: str = "",
                 init_from_checkpoint: bool = True,
                 checkpoint_path: str = "/tmp/spark-job-scheduler/",
                 skip_task_name_map: EnhancedOrderedDict = EnhancedOrderedDict()):
        self._unique_name = unique_name
        self._desc = desc
        self._init_from_checkpoint = init_from_checkpoint
        self._checkpoint_path = checkpoint_path
        self._skip_task_name_map = skip_task_name_map
        self._task_list = []  # [ScheduledTask]

    def schedule(self, scheduled_task: ScheduledTask):
        for task in self.task_list:
            if task.unique_name == scheduled_task.unique_name:
                raise Exception("scheduler中的任务名称["+ scheduled_task.unique_name +"]必须全局唯一！")
                return self
        self._task_list.append(scheduled_task)
        return self

    def has_next(self) -> bool:
        return self.get_first_need_running_task() is not None

    def next(self):
        task = self.get_first_need_running_task()
        if task is not None:
            return task.call()
        else:
            return None

    def process(self) -> bool:
        start_date = DateUtils.now()
        self.print_scheduler(start_date, None)
        if self.init_from_checkpoint:
            self.restore_checkpoint()
        while self.has_next():
            self.next()
            self.save_checkpoint()
        end_date = DateUtils.now()
        self.print_scheduler(start_date, end_date)
        return True

    def save_checkpoint(self):
        # TODO
        pass

    def restore_checkpoint(self):
        # TODO
        pass

    def get_first_need_running_task(self):
        # 实时取第一个应该执行的任务(ready | running), 没有就返回null
        task: ScheduledTask = None
        for item in self.task_list:
            if task is None \
                    and not self.skip_task_name_map.get(item.unique_name) \
                    and (item.status == TaskStatusEnum.READY or item.status == TaskStatusEnum.RUNNING):
                task = item
                return task
        return task

    def print_scheduler(self, process_start_date: datetime, process_end_date: datetime):
        print("**********************************************************************************************************************")
        print("**scheduler["+ self.unique_name +"]**"+ self.desc +"**: initFromCheckpoint=" + str(self.init_from_checkpoint)
                + ", checkpointPath=" + self.checkpoint_path + ", skipTaskNameMap=" + str(self.skip_task_name_map))
        left_str = "**scheduler["+ self.unique_name +"]**作业调度开始时间: " + DateUtils.to_str(process_start_date, format="%Y-%m-%d %H:%M:%S.%f")[:-3]
        if process_end_date is not None:
            left_str += ", 作业调度结束时间: " + DateUtils.to_str(process_end_date, format="%Y-%m-%d %H:%M:%S.%f")[:-3] + ", 作业调度总耗时: " \
                        + str(DateUtils.to_int(process_end_date)-DateUtils.to_int(process_start_date)) + "s"
        print(left_str)
        for task in self.task_list:
            task_str = "**scheduled task[" + task.unique_name + "]**" + task.desc + "**, 序号: " + str(task.ordered) + ", 状态: " + str(task.status) \
                      + ", 运行时信息: " + task.run_info + ", 开始时间: "
            if task.start_time is not None:
                task_str += DateUtils.to_str(task.start_time, format="%Y-%m-%d %H:%M:%S.%f")[:-3]
            else:
                task_str += "None"
            task_str += ", 结束时间: "
            if task.end_time is not None:
                task_str += DateUtils.to_str(task.end_time, format="%Y-%m-%d %H:%M:%S.%f")[:-3]
            else:
                task_str += "None"
            task_str += ", 耗时: "
            if task.start_time is not None and task.end_time is not None:
                task_str += str(DateUtils.to_int(task.end_time) - DateUtils.to_int(task.start_time))
            else:
                task_str += "0"
            task_str += "s"
            print(task_str)
        left_str = "**spark job scheduler [" + self.unique_name + "] process "
        if process_end_date is None:
            left_str += "starting......"
        else:
            left_str += "end!"
        print(left_str)
        print("**********************************************************************************************************************")


if __name__ == '__main__':
    # 业务配置初始化
    out_state = 1000

    # 业务回调函数，可以只读方式读取到函数外部定义的变量值
    def foo1():
        out_state = 30
        print(">>>>1>>>" + str(out_state))
        return ScheduledTaskResult()

    def foo2():
        print(">>>>2>>>" + str(out_state))
        return ScheduledTaskResult()
    # 构建任务Pipeline
    skip_task_name_map = EnhancedOrderedDict()
    skip_task_name_map["foo1"] = False
    skip_task_name_map["foo2"] = False
    scheduler = SparkJobScheduler(unique_name="SampleScheduler",
                                  desc="Spark简单调度器例子",
                                  init_from_checkpoint=False,
                                  checkpoint_path="./",
                                  skip_task_name_map=skip_task_name_map)
    scheduler.schedule(
        ScheduledTask(unique_name="foo1", desc="第1个任务", ordered=1, status=TaskStatusEnum.READY, callable=foo1)
    ).schedule(
        ScheduledTask(unique_name="foo2", desc="第2个任务", ordered=2, status=TaskStatusEnum.READY, callable=foo2)
    ).schedule(
        ScheduledTask(unique_name="CleanJob", desc="清理运行时环境", ordered=99, status=TaskStatusEnum.READY, callable=default_scheduled_callable_func)
    ).process()
