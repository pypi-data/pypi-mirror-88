# -*- coding:utf-8 -*-
import time
import datetime as dt
from datetime import datetime
from typing import Union, NoReturn, List


class DateUtils:

    @staticmethod
    def to_int(datetime: datetime) -> int:
        # 转换成时间秒, 用time.time()可以返回有小数点如0.1的秒整数
        return int(time.mktime(datetime.timetuple()))

    @staticmethod
    def int_to_datetime(datetime_int: int) -> datetime:
        return datetime.fromtimestamp(datetime_int)

    @staticmethod
    def str_to_datetime(datetime_str: str, format="%Y%m%d%H%M%S") -> datetime:
        """
        日期字符转换为日期
        :param datetime_str 日期字符
        :param format e.g. "%Y-%m-%d"
        :return datetime
        """
        return datetime.strptime(datetime_str, format)

    @staticmethod
    def to_str(date_time: Union[datetime, datetime.date], format="%Y%m%d%H%M%S") -> str:
        """
        e.g. DateUtils.to_str(DateUtils.now(), format="%Y-%m-%d %H:%M:%S.%f")[:-3] = "2019-01-22 00:49:25.216"
        :param date_time: date_time类型， 如果是字符串类型则直接返回
        :param format: "%Y-%m-%d" 或 "%Y%m%d%H%M%S.%f" 格式为 "年月日时分秒.6位毫秒" 经[:-3]可以变为3位毫秒
        :return:
        """
        return date_time.strftime(format)  # 转成字面整型字符串, e.g. date: 2009-12-08 16:34:00 -> '20091208163400'

    @staticmethod
    def now() -> datetime:
        return datetime.now()

    @staticmethod
    def now_to_int() -> int:
        return DateUtils.to_int(DateUtils.now())

    @staticmethod
    def now_to_str() -> str:
        """当前时间转成string格式输出，如：2019-07-24 09:19:09.668136"""
        return DateUtils.to_str(DateUtils.now(), format="%Y-%m-%d %H:%M:%S.%f")

    @staticmethod
    def now_to_ymd_str() -> str:
        """当前时间转成string格式输出，如：2019-07-24"""
        return DateUtils.to_str(DateUtils.now(), format="%Y-%m-%d")

    @staticmethod
    def calc_duration_seconds(start_time_int: int, end_time_int: int) -> int:
        """
        :param start_time_int:
        :param end_time_int:
        :return:
        usage:
            start_time_int = DateUtils.to_int(DateUtils.now())
            DateUtils.sleep(5)
            duration = DateUtils.calc_duration_seconds(start_time_int, DateUtils.to_int(DateUtils.now()))
            print(duration)
        """
        return end_time_int - start_time_int

    @staticmethod
    def calc_delta_days(start_date: datetime=None, end_date: datetime=None, include_start_end_date: bool=False) -> List[str]:
        """
        计算从start_date到end_date的所有日期数组（包含start_date, end_date）
        :param start_date e.g. 2020-11-03
        :param end_date e.g. 2020-11-03
        :param include_start_end_date 返回的list是否包含start_date和end_date
        :return List[str]
        """
        if type(start_date) is str:
            start_date = DateUtils.str_to_datetime(start_date, "%Y-%m-%d")
        if type(end_date) is str:
            end_date = DateUtils.str_to_datetime(end_date, "%Y-%m-%d")
        timedelta = end_date - start_date
        if include_start_end_date:
            return [start_date + dt.timedelta(days=int(i)) for i in range(0, timedelta.days+1)]
        else:
            return [start_date + dt.timedelta(days=int(i)) for i in range(1, timedelta.days)]

    @staticmethod
    def add_date(start_date: Union[datetime, datetime.date], days: int = 1) -> Union[datetime, datetime.date]:
        """
        增加days天数后的日期
        :param start_date 起始日期
        :param days 增加的天数，可以为负数
        :return datetime or date 新的日期
        """
        return start_date + dt.timedelta(days)

    @staticmethod
    def is_weekend(date: datetime) -> bool:
        """
        判断指定日期是否周六或周日的日期
        :param date e.g. 2020-07-26
        """
        if type(date) is str:
            date = DateUtils.str_to_datetime(date, format="%Y-%m-%d")
        week_day_num: int = date.weekday() + 1
        return week_day_num == 6 or week_day_num == 7

    @staticmethod
    def is_type_datetime(date: datetime) -> bool:
        return type(date) is datetime

    @staticmethod
    def sleep(seconds) -> NoReturn:
        time.sleep(seconds)


if __name__ == '__main__':
    print(DateUtils.add_date(DateUtils.now().date(), -1))
    print(DateUtils.to_str(DateUtils.now(), format="%Y-%m-%d %H:%M:%S.%f")[:-3])
    start_date = DateUtils.str_to_datetime("20180302", "%Y%m%d")
    delta_day_list = DateUtils.calc_delta_days(start_date, DateUtils.now(), True)
    for day in delta_day_list[-20:]:
        print(f"final 20 delta day：{DateUtils.to_str(day, '%Y-%m-%d')}, is_week_day：{DateUtils.is_weekend(day)}")
    duration = DateUtils.calc_duration_seconds(DateUtils.now_to_int(), DateUtils.to_int(DateUtils.str_to_datetime('20190109234900')))
    print(duration)
