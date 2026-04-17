"""Day 6 公共依赖。"""

from dataclasses import dataclass

from fastapi import Query


@dataclass
class PaginationParams:
    """分页参数对象。"""

    skip: int
    limit: int


def get_pagination(
    skip: int = Query(default=0, ge=0, description="跳过多少条记录"),
    limit: int = Query(default=10, ge=1, le=100, description="每页多少条记录"),
) -> PaginationParams:
    """封装分页参数依赖。

    后面做更多列表接口时，就不需要在每个接口里重复写分页逻辑。
    """

    return PaginationParams(skip=skip, limit=limit)
