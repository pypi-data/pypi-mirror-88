# -*- coding:utf-8 -*-
from collections import OrderedDict
from skydl.common.common_utils import CommonUtils
from typing import List, Union, MutableMapping, TypeVar, NoReturn, Tuple

K = TypeVar('K')
V = TypeVar('V')


class EnhancedOrderedDict(OrderedDict, MutableMapping[K, V]):
    """
    增强功能的OrderedDict，支持Type hint、subset等功能
    """
    def subset(self, items=[]) -> "EnhancedOrderedDict[K, V]":
        """返回subset的deep copy对象"""
        if items is None or len(items) < 1:
            # return self.copy()  # 是否应该返回空的OrderedDic()，即EnhancedOrderedDict()
            return EnhancedOrderedDict()
        all = super(EnhancedOrderedDict, self).items()
        # return type(self)((key, value) for (key, value) in all if key in items)
        copied_order_dict = EnhancedOrderedDict()
        for key, value in all:
            if key in items:
                copied_order_dict[key] = CommonUtils.deepcopy(value)
        return copied_order_dict

    def to_list(self) -> List[Tuple[K, V]]:
        """convert OrderedDict's items to list:[(key1,value1), (key2,value2)...]"""
        return list(self.items())

    def next_key(self, key: K) -> Union[K, None]:
        all_keys = list(self.keys())
        if key in all_keys:
            key_index = all_keys.index(key)
        if key_index+1 <= len(all_keys) - 1:
            return all_keys[key_index + 1]
        else:
            return None

    def prev_key(self, key: K) -> Union[K, None]:
        all_keys = list(self.keys())
        if key in all_keys:
            key_index = all_keys.index(key)
        if key_index-1 >= 0:
            return all_keys[key_index - 1]
        else:
            return None

    def put(self, key: K, value: V) -> NoReturn:
        """put操作"""
        self.__setitem__(key, value)

    def remove(self, key: K) -> NoReturn:
        """删除指定的key元素"""
        self.__delitem__(key)

    def contains(self, key: K) -> bool:
        """是否包含指定的key"""
        return self.__contains__(key)


if __name__ == '__main__':
    abc = EnhancedOrderedDict({'a': 1, 'b': 2, 'c': 4})
    print(f"first key: {list(abc.items())[0][0]}, first value: {list(abc.items())[0][1]}")
    for key in abc:
        print(f"only get key={key}")
    for value in abc.values():
        print(f"only get value={value}")
    for key, value in abc.items():
        print(f"get items: key={key}, value={value}")
    nested_map: EnhancedOrderedDict[str, EnhancedOrderedDict[str, int]] = EnhancedOrderedDict(test=EnhancedOrderedDict(test1123=111), test1=EnhancedOrderedDict(test1123=222))
    nested_map.put("aaa", EnhancedOrderedDict(test1123=0.123))
    print(f"len={len(nested_map)}, contains(aaa)={nested_map.contains('aaa')}")
    nested_map = nested_map.subset(['aaa'])
    print(f"nested_map.get('test').get('test123')={nested_map.get('aaa').get('test1123')}")
    mod = EnhancedOrderedDict(banana=3, apple=4, pear=1, orange=2)
    mod["watermelon"] = 10
    print("apple next_key=" + str(mod.next_key("orange")))
    print("apple prev_key=" + str(mod.prev_key("orange")))
    print(list(mod.keys()).index("pear"))
    print(f"mod.prev_key.value: {mod.to_list()[-2][1]}")
    print(mod.get("apple"))
    print(mod.subset())
    print("####test copy")
    a = ["1", "2"]
    original_mod = EnhancedOrderedDict(banana=a)
    copied_mod = original_mod.subset(["apple", "banana"])
    a.append("new value")
    print("original_mod", original_mod)
    print("copied_mod", copied_mod)
