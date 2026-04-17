"""Day 4 的模拟数据层。

这里先用内存列表模拟数据库，
目的是把注意力放在路由、参数和校验上。
"""

fake_users_db = [
    {"id": 1, "name": "Minda", "age": 24, "role": "student", "city": "Hangzhou"},
    {"id": 2, "name": "Tom", "age": 26, "role": "developer", "city": "Shanghai"},
    {"id": 3, "name": "Alice", "age": 22, "role": "student", "city": "Beijing"},
]
