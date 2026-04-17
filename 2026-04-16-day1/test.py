"""Day 1 模块示例。

这个文件的存在是为了演示：
1. 一个 `.py` 文件就是一个模块
2. 其他文件可以通过 import 使用这里的函数
3. 函数可以接收参数并返回结果
"""


def format_greeting(name: str) -> str:
    """返回一段欢迎语。

    参数:
        name: 学习者的名字

    返回:
        一段格式化后的字符串
    """

    return f"你好，{name}，欢迎开始 Python 第一天学习。"


def build_learning_profile(name: str, direction: str) -> dict[str, str]:
    """构造一个简单的学习者信息字典。

    这里返回字典，是因为字典很适合描述一个对象的多个属性。
    """

    return {
        "name": name,
        "direction": direction,
        "current_day": "Day 1",
    }
