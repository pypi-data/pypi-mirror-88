# -*- coding:utf-8 -*-
import os
import copy
import math
from pathlib import Path
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from typing import List
from skydl.common.option import Option


class CommonUtils:

    @staticmethod
    def cycle(iterable=[None]):
        """
        e.g.
        from skydl.common.common_utils import CommonUtils
        ...
        iter = CommonUtils.cycle([0,2,3,1])
        next(iter)->0,next(iter)->2,...,next(iter)->0,next(iter)->2,...
        :param iterable: e.g. [0,2,3,1]
        :return:
        """
        from itertools import cycle
        return cycle(iterable)

    @staticmethod
    def camelcase_to_snakecase(class_name):
        """
        Convert camel-case string to snake-case.
        e.g. SuperDatasetBuilder.camelcase_to_snakecase(RecommendDatasetBuilder().__class__.__name__)
        -> "recommend_dataset_builder"
        or SuperDatasetBuilder.camelcase_to_snakecase("RecommendDatasetBuilder")
        -> "recommend_dataset_builder"
        """
        # @see tensorflow_datasets.core.naming#camelcase_to_snakecase
        import re
        _first_cap_re = re.compile("(.)([A-Z][a-z0-9]+)")
        _all_cap_re = re.compile("([a-z0-9])([A-Z])")
        s1 = _first_cap_re.sub(r"\1_\2", class_name)
        return _all_cap_re.sub(r"\1_\2", s1).lower()

    @staticmethod
    def deepcopy(x, memo=None, _nil=[]):
        """深拷贝，该方法执行比较耗时间，应谨慎使用"""
        return copy.deepcopy(x, memo, _nil)

    @staticmethod
    def format_number(x, times=1, format_args="0.2f", use_round_down=True):
        """
        格式化数字输出, e.g. 12.3456->"12.34"
        :param x: 数字 e.g. 12.3456
        :param times: 乘以的倍数，方便%输出
        :param format_args: e.g. "0.2f" 保留小数点后2位输出 e.g. 123.465->"123.47"
        :param use_round_down True直接截取, False四舍五入 e.g. False: 99.999989->'100.00', 99.11789->'99.12'
        :return: "12.34" 如果要to float类型就用: float(format_number(12.3456, 100)), 注意float("100.0000")->100.0
        """
        if x is None or math.isnan(x):
            return "0.00"
        try:
            # 最原始的四舍五入的方法：return format(float(x)*times, format_args)
            # 用Decimal精确截取小数点后2位小数，也可以四舍五入。e.g. 123.465->"123.46"
            rounding = ROUND_DOWN if use_round_down else ROUND_HALF_UP
            return str(Decimal(float(x) * times).quantize(Decimal(format(0, format_args)), rounding=rounding))
        except:
            return str(x)

    @staticmethod
    def isnan(value):
        try:
            return math.isnan(float(value))
        except:
            return False

    @staticmethod
    def get_user_home_path(default_value: str = "/tmp") -> str:
        """
        get user home
        :param default_value the default value
        :return str
        """
        return str(Option(Path.home()).get_or_else(default_value))

    @staticmethod
    def path_exists(path: str) -> bool:
        """
        文件或路径是否在本地环境存在
        :param path 文件名或路径 e.g. "/xxx/a.json" or "/xxx"
        :return bool true-存在 false-不存在
        """
        return os.path.exists(Option(path).get_or_else(""))

    @staticmethod
    def calc_batch_size(num_total: int = 1, num_partitions: int = 1) -> int:
        """
        * 计算batch size，包括最后数量不足的那一批
        * e.g. calcBatchSize(20,8)=3,calcBatchSize(20,20)=1,calcBatchSize(20,15)=2,calcBatchSize(20,5)=4,
        * calcBatchSize(20,100)=1,calcBatchSize(20,-2)=-10
        * @param num_total 总数
        * @param num_partitions 分区数
        * @return batch_size
        """
        return int(math.ceil(float(num_total) / float(num_partitions)))

    @staticmethod
    def total_num_batch(num_total, batch_size, allow_smaller_final_batch=False) -> int:
        """
        计算总的批次数
        :param num_total 总数
        :param batch_size 每批的size
        :param allow_smaller_final_batch 允许最后不足批的数
        :return num_batch
        """
        num_batch = num_total // batch_size
        if allow_smaller_final_batch:
            if num_total > (num_batch * batch_size):
                return num_batch + 1
            else:
                return num_batch
        else:
            # 舍去最后不能够成1批的剩余训练数据部分
            return num_batch

    @staticmethod
    def batch_index_split(num_total: int, batch_size: int, begin_index: int = 0) -> List[List[int]]:
        """
        * 对index分批，可以作分页用
        * e.g. 有数据的index范围是lowerbound=12, upperbound=1001, numPartitions=5，则totalLen=upperbound-lowerbound+1,
        * 则分批函数为batch_index_split(1001-12+1, calc_batch_size(1001-12+1,5), 12),
        * 最后分批结果为：List[List[Long]] = List(List(12, 209, 0), List(210, 407, 1), List(408, 605, 2), List(606, 803, 3), List(804, 1001, 4))
        usage:
        ```
        assert 3 == SparkWrapper.total_num_batch(13, SparkWrapper.calc_batch_size(13, 3), True)
        batched_indexes: List[List[int]] = SparkWrapper.batch_index_split(13, SparkWrapper.calc_batch_size(13, 3))
        for batch in batched_indexes:
            begin_index = batch[0]
            end_index = batch[1]
            page_index = batch[2]
            print(f"page_index：{page_index}, begin_index：{begin_index}，end_index={end_index}")
            for data_index in range(begin_index, end_index+1):
                print(f"data index: {data_index}")
        ```
        *
        * :param num_total e.g. 10
        * :param batch_size e.g. 3
        * :param begin_index 第1页从第几个index的元素开始 e.g. 0
        * :return batched_indexes List[List[begin_index, end_iIndex, batched_num(即页次)]]
        """
        num_batch: int = int(math.ceil(float(num_total) / float(batch_size)))
        batched_indexs: List[List[int]] = []
        for row in range(0, num_batch):
            end_index = (row + 1) * batch_size - 1 + begin_index
            batched_indexs.append(
                [row*batch_size + begin_index,
                 end_index if end_index < (num_total-1+begin_index) else num_total-1+begin_index,
                 row]
            )
        return batched_indexs


if __name__ == '__main__':
    print(CommonUtils.path_exists("/"))
    print(CommonUtils.isnan(float("nan")))
    # 计算批次
    assert 3 == CommonUtils.total_num_batch(13, CommonUtils.calc_batch_size(13, 3), True)
    batched_indexes: List[List[int]] = CommonUtils.batch_index_split(13, CommonUtils.calc_batch_size(13, 3))
    for batch in batched_indexes:
        begin_index = batch[0]
        end_index = batch[1]
        page_no = batch[2]
        print(f"page_no：{page_no}, begin_index：{begin_index}，end_index={end_index}")
        for data_index in range(begin_index, end_index+1):
            print(f"data index: {data_index}")


