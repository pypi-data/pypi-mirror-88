# -*- coding:utf-8 -*-

class Option:
    """实现Option功能"""
    def __init__(self, value):
        self._value = value

    def get_or_else(self, default_value=None):
        return self._value if self.non_empty() else default_value

    def get(self):
        return self._value

    def is_empty(self) -> bool:
        return self._value is None

    def non_empty(self) -> bool:
        return self._value is not None


if __name__ == '__main__':
    print(f"Option(1).get()={Option(None).get_or_else(222)}")
    print(f"Option(1).get()={Option(False).get_or_else(123)}")
