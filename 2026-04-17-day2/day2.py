"""Day 2 Python 后端常见写法示例。

这个文件会把第二天最重要的知识点串起来：
1. 类与对象
2. 类型注解
3. 异常处理
4. datetime 时间处理
5. 常用标准库
6. async / await 和 asyncio

运行方式：
    python day2.py
"""

from __future__ import annotations

import asyncio
import json
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timedelta
from statistics import mean

from config_tools import ConfigError, build_base_url, load_app_config


class StudyDataError(Exception):
    """学习数据不合法时抛出的业务异常。"""


@dataclass
class LearningTask:
    """学习任务类。

    `@dataclass` 可以帮我们自动生成初始化方法，
    很适合这种“主要用来存数据”的类。
    """

    title: str
    minutes: int
    finished: bool = False


class User:
    """一个简单的用户类，用来演示类、对象、实例属性和实例方法。"""

    def __init__(self, name: str, direction: str) -> None:
        self.name = name
        self.direction = direction

        # field(default_factory=...) 常用于 dataclass。
        # 普通类里更常见的是在 __init__ 里自己初始化属性。
        self.tasks: list[LearningTask] = []

        # datetime.now() 是后端里非常常见的时间获取方式。
        self.created_at = datetime.now()

    def add_task(self, task: LearningTask) -> None:
        """给当前用户添加学习任务。"""

        self.tasks.append(task)

    def finish_task(self, title: str) -> bool:
        """根据任务标题把任务标记为完成。

        返回值:
            True 表示找到了任务并已更新
            False 表示没有找到对应任务
        """

        for task in self.tasks:
            if task.title == title:
                task.finished = True
                return True

        return False

    def get_total_minutes(self) -> int:
        """统计所有任务预计学习时长。"""

        return sum(task.minutes for task in self.tasks)

    def to_dict(self) -> dict[str, object]:
        """把对象转成字典，便于后面做 JSON 响应。"""

        return {
            "name": self.name,
            "direction": self.direction,
            "created_at": self.created_at.isoformat(timespec="seconds"),
            "task_count": len(self.tasks),
        }


def parse_minutes(raw_value: str) -> int:
    """把字符串转换为学习分钟数，并做基础校验。"""

    try:
        minutes = int(raw_value)
    except ValueError as error:
        raise StudyDataError(f"学习时长必须是整数，当前收到: {raw_value}") from error

    if minutes <= 0:
        raise StudyDataError("学习时长必须大于 0")

    return minutes


def create_demo_user() -> User:
    """创建一个带有示例任务的用户对象。"""

    user = User(name="Minda", direction="Python 后端")
    user.add_task(LearningTask(title="学习类与对象", minutes=30))
    user.add_task(LearningTask(title="练习异常处理", minutes=20))
    user.add_task(LearningTask(title="理解 async/await", minutes=40))
    user.finish_task("学习类与对象")
    return user


def show_class_and_type_hint_examples(user: User) -> None:
    """演示类、对象和类型注解。"""

    print("\n=== 1. 类、对象、类型注解 ===")
    print(f"用户信息: {user.to_dict()}")

    for task in user.tasks:
        print(f"任务: {task.title}, 分钟数: {task.minutes}, 是否完成: {task.finished}")


def show_exception_examples() -> None:
    """演示 try / except / else / finally 的基本用法。"""

    print("\n=== 2. 异常处理 ===")

    sample_values = ["25", "abc", "-5"]

    for value in sample_values:
        try:
            minutes = parse_minutes(value)
        except StudyDataError as error:
            print(f"输入 {value!r} 有问题: {error}")
        else:
            print(f"输入 {value!r} 转换成功，结果是 {minutes} 分钟")
        finally:
            print("这次输入处理结束")


def show_datetime_examples(user: User) -> None:
    """演示 datetime 和 timedelta 的常见用法。"""

    print("\n=== 3. datetime 时间处理 ===")

    now = datetime.now()
    next_review_time = now + timedelta(days=1, hours=2)

    print(f"当前时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"下次复习时间: {next_review_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"用户创建时间: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}")


def show_standard_library_examples(user: User) -> None:
    """演示几个后端里非常常见的标准库能力。"""

    print("\n=== 4. 标准库常用模块 ===")

    # statistics.mean 用来求平均值。
    task_minutes = [task.minutes for task in user.tasks]
    avg_minutes = mean(task_minutes)

    # Counter 用来做计数统计。
    finish_counter = Counter(task.finished for task in user.tasks)

    print(f"平均每个任务学习时长: {avg_minutes:.2f} 分钟")
    print(f"已完成任务数: {finish_counter[True]}")
    print(f"未完成任务数: {finish_counter[False]}")
    print(f"总学习时长: {user.get_total_minutes()} 分钟")


def show_config_module_example() -> None:
    """演示从单独模块读取配置文件。"""

    print("\n=== 5. 配置读取模块 ===")

    try:
        config = load_app_config("app_config.json")
    except ConfigError as error:
        print(f"读取配置失败: {error}")
        return

    print(f"配置内容: {config}")
    print(f"应用基础地址: {build_base_url(config)}")


def build_task_summary(name: str, total_tasks: int, prefix: str = "今日计划") -> str:
    """演示默认参数和关键字参数。

    这类函数写法在后面封装工具函数、服务函数时非常常见。
    """

    return f"{prefix}: {name} 有 {total_tasks} 个任务"


def show_json_and_argument_examples(user: User) -> None:
    """演示 JSON 转换和函数参数写法。"""

    print("\n=== 5.1 JSON 和函数参数 ===")

    user_dict = user.to_dict()

    # json.dumps() 把 Python 对象转成 JSON 字符串。
    user_json = json.dumps(user_dict, ensure_ascii=False)

    # json.loads() 把 JSON 字符串重新转回 Python 对象。
    restored_user = json.loads(user_json)

    print(f"用户字典: {user_dict}")
    print(f"JSON 字符串: {user_json}")
    print(f"还原后的对象: {restored_user}")

    # 位置参数调用。
    print(build_task_summary(user.name, len(user.tasks)))

    # 关键字参数调用。
    print(
        build_task_summary(
            name=user.name, total_tasks=len(user.tasks), prefix="复习安排"
        )
    )


async def fake_request(task_name: str, delay_seconds: float) -> str:
    """模拟一个异步请求。

    asyncio.sleep() 不会阻塞整个事件循环，
    所以多个任务可以在等待期间交替执行。
    """

    await asyncio.sleep(delay_seconds)
    return f"{task_name} 已完成，耗时 {delay_seconds} 秒"


async def show_async_examples() -> None:
    """演示 async / await 和 asyncio.gather。"""

    print("\n=== 6. 异步编程基础 ===")

    # 先演示顺序等待。
    start = time.perf_counter()
    result_1 = await fake_request("读取用户信息", 1)
    result_2 = await fake_request("读取课程信息", 1)
    sequential_cost = time.perf_counter() - start

    print("顺序执行结果:")
    print(result_1)
    print(result_2)
    print(f"顺序执行耗时: {sequential_cost:.2f} 秒")

    # 再演示并发等待。
    start = time.perf_counter()
    parallel_results = await asyncio.gather(
        fake_request("读取用户信息", 1),
        fake_request("读取课程信息", 1),
    )
    parallel_cost = time.perf_counter() - start

    print("并发执行结果:")
    for result in parallel_results:
        print(result)
    print(f"并发执行耗时: {parallel_cost:.2f} 秒")


def main() -> None:
    """把 Day 2 的所有示例串起来执行。"""

    print("Python Day 2 学习示例开始")

    user = create_demo_user()
    show_class_and_type_hint_examples(user)
    show_exception_examples()
    show_datetime_examples(user)
    show_standard_library_examples(user)
    show_config_module_example()
    show_json_and_argument_examples(user)

    # asyncio.run() 会帮我们创建并运行事件循环。
    asyncio.run(show_async_examples())

    print("\nPython Day 2 学习示例结束")


if __name__ == "__main__":
    main()
