"""前五天异步补漏示例。

运行:
    python3 async_demo.py
"""

from __future__ import annotations

import asyncio
import time


async def non_blocking_task(name: str, delay: float) -> str:
    """正确示例: 使用 asyncio.sleep，不阻塞事件循环。"""

    await asyncio.sleep(delay)
    return f"{name} 完成，等待 {delay} 秒"


async def blocking_task(name: str, delay: float) -> str:
    """错误示例: 在协程里直接使用 time.sleep。"""

    time.sleep(delay)
    return f"{name} 完成，但它阻塞了事件循环 {delay} 秒"


async def sequential_demo() -> None:
    print("\n=== 1. 顺序等待 ===")
    start = time.perf_counter()
    result_1 = await non_blocking_task("任务 A", 1)
    result_2 = await non_blocking_task("任务 B", 1)
    cost = time.perf_counter() - start

    print(result_1)
    print(result_2)
    print(f"顺序等待耗时: {cost:.2f} 秒")


async def concurrent_demo() -> None:
    print("\n=== 2. 正确并发等待 ===")
    start = time.perf_counter()
    results = await asyncio.gather(
        non_blocking_task("任务 A", 1),
        non_blocking_task("任务 B", 1),
    )
    cost = time.perf_counter() - start

    for result in results:
        print(result)
    print(f"并发等待耗时: {cost:.2f} 秒")


async def blocked_event_loop_demo() -> None:
    print("\n=== 3. 协程里误用阻塞代码 ===")
    start = time.perf_counter()
    results = await asyncio.gather(
        blocking_task("任务 A", 1),
        blocking_task("任务 B", 1),
    )
    cost = time.perf_counter() - start

    for result in results:
        print(result)
    print(f\"表面上用了 gather，但总耗时还是: {cost:.2f} 秒\")


async def main() -> None:
    await sequential_demo()
    await concurrent_demo()
    await blocked_event_loop_demo()


if __name__ == "__main__":
    asyncio.run(main())
