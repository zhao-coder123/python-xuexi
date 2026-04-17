"""Day 7 用户模型。"""

from dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str
    age: int
    role: str
    city: str
