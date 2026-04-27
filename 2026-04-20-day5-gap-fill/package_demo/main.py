"""包入口示例。

推荐运行:
    python3 -m package_demo.main
"""

from __future__ import annotations

from package_demo.services import build_demo_learner, summarize_learner


def main() -> None:
    learner = build_demo_learner()
    summary = summarize_learner(learner)

    print("=== package_demo 运行成功 ===")
    print("这说明当前目录里的包导入路径是稳定的。")
    print(summary)

    print("\n任务列表:")
    for index, task in enumerate(learner.tasks, start=1):
        print(
            f"{index}. {task.title} | {task.minutes} 分钟 | 已完成: {task.finished}"
        )


if __name__ == "__main__":
    main()
