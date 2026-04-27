"""包内服务模块示例。"""

from __future__ import annotations

from package_demo.models import Learner, LearningTask


def build_demo_learner() -> Learner:
    learner = Learner(name="Minda", direction="Python 后端")
    learner.tasks.append(LearningTask(title="理解包和模块", minutes=20, finished=True))
    learner.tasks.append(LearningTask(title="练习 python -m", minutes=15))
    learner.tasks.append(LearningTask(title="理解绝对导入", minutes=25))
    return learner


def summarize_learner(learner: Learner) -> dict[str, object]:
    return {
        "name": learner.name,
        "direction": learner.direction,
        "task_count": len(learner.tasks),
        "total_minutes": learner.total_minutes(),
        "finished_count": sum(task.finished for task in learner.tasks),
    }
