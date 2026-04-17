"""Day 2 配置读取模块示例。

这个文件用来演示几个 Day 2 的重点：
1. 标准库 `json`
2. 标准库 `pathlib`
3. 自定义异常
4. 带类型注解的函数
"""

from __future__ import annotations

import json
from pathlib import Path


class ConfigError(Exception):
    """配置文件有问题时抛出的自定义异常。"""


REQUIRED_KEYS = ["app_name", "debug", "port"]


def load_app_config(file_name: str) -> dict[str, object]:
    """读取并校验 JSON 配置文件。

    参数:
        file_name: 配置文件名，比如 `app_config.json`

    返回:
        解析后的配置字典

    异常:
        ConfigError: 当文件不存在、JSON 格式错误、缺少必须字段时抛出
    """

    # __file__ 代表当前这个 Python 文件自己的路径。
    # Path(__file__).resolve().parent 可以拿到当前文件所在目录。
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / file_name

    if not config_path.exists():
        raise ConfigError(f"配置文件不存在: {config_path}")

    try:
        content = config_path.read_text(encoding="utf-8")
        config = json.loads(content)
    except json.JSONDecodeError as error:
        raise ConfigError(f"配置文件不是合法 JSON: {error}") from error

    for key in REQUIRED_KEYS:
        if key not in config:
            raise ConfigError(f"配置文件缺少必须字段: {key}")

    return config


def build_base_url(config: dict[str, object]) -> str:
    """根据配置拼接一个基础 URL。"""

    port = config["port"]
    return f"http://127.0.0.1:{port}"
