"""Day 5 自定义异常定义。"""


class AppException(Exception):
    """业务异常。

    这个异常类的目的不是替代所有异常，
    而是把“我们希望返回给前端的业务错误”统一起来。
    """

    def __init__(self, message: str, code: int, status_code: int) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)
