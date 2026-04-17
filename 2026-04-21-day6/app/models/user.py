"""Day 6 用户模型。"""

from dataclasses import dataclass


@dataclass
class User:
    """用 dataclass 表示领域模型。"""

    id: int
    name: str
    age: int
    role: str
    city: str
