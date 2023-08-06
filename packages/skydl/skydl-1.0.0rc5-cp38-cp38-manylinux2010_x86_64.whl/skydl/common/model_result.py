# -*- coding: utf-8 -*-
from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')


@dataclass
class ModelResult(Generic[T]):
    """API统一返回的模型对象"""
    is_success: bool = False
    code: str = ""
    msg: str = ""
    data: T = None

    def with_model(self, model: T) -> "ModelResult":
        self.is_success = True
        self.data = model
        return self

    def get_model(self) -> T:
        return self.data

    def with_error(self, error_code: str = "", error_msg: str = "") -> "ModelResult":
        self.is_success = False
        self.code = error_code
        self.msg = error_msg
        return self


if __name__ == '__main__':
    result: ModelResult[list] = ModelResult().with_model([123])
    print(result.get_model())
