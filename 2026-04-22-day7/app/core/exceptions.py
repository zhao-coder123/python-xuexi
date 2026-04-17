"""Day 7 自定义异常。"""


class AppException(Exception):
    def __init__(self, message: str, code: int, status_code: int) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)
