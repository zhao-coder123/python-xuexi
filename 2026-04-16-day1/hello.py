"""Day 1 Python 入门示例。

这个文件专门演示第一天最应该掌握的内容：
1. 变量和常见数据类型
2. 函数的定义与调用
3. 模块导入
4. 列表、字典、元组、集合
5. 条件判断和循环
6. `if __name__ == "__main__"` 的作用

运行方式：
    python hello.py
"""

from test import build_learning_profile, format_greeting


# 常量通常使用全大写命名。
# 这里表示这个名字在整个脚本运行期间都不会被修改。
STUDENT_NAME = "Minda"


def show_basic_types() -> None:
    """演示 Python 最常见的基础数据类型。"""

    print("\n=== 1. 基础数据类型 ===")

    # 字符串：保存文本内容。
    course_name = "Python Day 1"

    # 整数：保存没有小数的数字。
    study_minutes = 90

    # 浮点数：保存带小数的数字。
    progress_score = 7.5

    # 布尔值：只有 True 和 False，常用于条件判断。
    has_started = True

    # None 表示“当前没有值”。
    next_topic = None

    # 用 type() 可以查看变量的实际类型。
    print(f"course_name = {course_name}, type = {type(course_name).__name__}")
    print(f"study_minutes = {study_minutes}, type = {type(study_minutes).__name__}")
    print(f"progress_score = {progress_score}, type = {type(progress_score).__name__}")
    print(f"has_started = {has_started}, type = {type(has_started).__name__}")
    print(f"next_topic = {next_topic}, type = {type(next_topic).__name__}")


def show_string_and_conversion_examples() -> None:
    """演示字符串常见操作和基础类型转换。"""

    print("\n=== 1.1 字符串和类型转换 ===")

    raw_name = "  minda python  "
    age_text = "18"

    # strip() 去掉首尾空格。
    clean_name = raw_name.strip()

    # upper() / replace() / split() 都是字符串里非常常见的方法。
    print(f"原始字符串: {raw_name!r}")
    print(f"去掉空格后: {clean_name!r}")
    print(f"转大写: {clean_name.upper()}")
    print(f"替换后: {clean_name.replace('python', 'backend')}")
    print(f"切分后: {clean_name.split()}")

    # 后端里经常会把请求参数从字符串转换成数字。
    age_number = int(age_text)
    score_text = str(99)

    print(f"age_text = {age_text}, type = {type(age_text).__name__}")
    print(f"age_number = {age_number}, type = {type(age_number).__name__}")
    print(f"score_text = {score_text}, type = {type(score_text).__name__}")


def show_containers() -> list[str]:
    """演示容器类型，并返回任务列表供后面的函数继续使用。"""

    print("\n=== 2. 容器类型 ===")

    # 列表 list：有顺序、可重复、可修改，适合保存一组数据。
    tasks = ["安装 Python", "创建虚拟环境", "运行 hello.py"]

    # append() 会把新元素追加到列表末尾。
    tasks.append("看懂基础语法")

    # 字典 dict：键值对结构，适合描述“一个对象”。
    student = {
        "name": STUDENT_NAME,
        "role": "Python 初学者",
        "goal": "先学会写基础脚本，再进入 FastAPI",
    }

    # 元组 tuple：有顺序，但不可修改，适合表示固定数据。
    screen_size = (1920, 1080)

    # 集合 set：无序、不重复，适合做去重。
    tags = {"python", "python", "fastapi", "backend"}

    print(f"tasks = {tasks}")
    print(f"student = {student}")
    print(f"screen_size = {screen_size}")
    print(f"tags = {tags}")

    # 取字典中的值时，常用键名访问。
    print(f"学生名字: {student['name']}")

    # len() 可以统计容器中元素的数量。
    print(f"任务数量: {len(tasks)}")

    return tasks


def show_control_flow(tasks: list[str]) -> None:
    """演示条件判断和循环。"""

    print("\n=== 3. 条件判断和循环 ===")

    # if / else 用来根据条件执行不同逻辑。
    if len(tasks) >= 4:
        print("今天的任务已经比较完整了。")
    else:
        print("今天的任务还可以再补一点。")

    # enumerate() 可以在循环时同时拿到序号和元素。
    for index, task in enumerate(tasks, start=1):
        print(f"第 {index} 个任务: {task}")


def show_functions_and_modules(tasks: list[str]) -> None:
    """演示函数调用和模块导入。"""

    print("\n=== 4. 函数和模块 ===")

    # 这里调用的是 test.py 中定义的函数。
    greeting = format_greeting(STUDENT_NAME)
    profile = build_learning_profile(STUDENT_NAME, "Python 后端")

    print(greeting)
    print(f"学习档案: {profile}")

    # 函数也可以处理传入的数据，这里统计任务列表的前两个任务。
    print(f"优先完成: {tasks[:2]}")


def main() -> None:
    """主函数：把今天要演示的知识点按顺序串起来。"""

    print("Python Day 1 学习示例开始")

    show_basic_types()
    show_string_and_conversion_examples()
    tasks = show_containers()
    show_control_flow(tasks)
    show_functions_and_modules(tasks)

    print("\nPython Day 1 学习示例结束")


# 这一段是 Python 初学者必须理解的经典写法。
# 当你直接运行 `python hello.py` 时，__name__ 的值会是 "__main__"，于是 main() 会执行。
# 但如果 hello.py 被别的文件 import，这里的代码就不会自动执行。
if __name__ == "__main__":
    main()
