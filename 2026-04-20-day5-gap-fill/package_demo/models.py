"""包内数据模型示例。"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LearningTask:
    title: str
    minutes: int
    finished: bool = False


@dataclass
class Learner:
    name: str
    direction: str
    tasks: list[LearningTask] = field(default_factory=list)

    def total_minutes(self) -> int:
        return sum(task.minutes for task in self.tasks)
