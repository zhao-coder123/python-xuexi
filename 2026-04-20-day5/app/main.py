"""Day 5: 统一响应、全局异常、文档示例入口。"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException
from app.core.response import error_response
from app.routers.users import router as users_router


app = FastAPI(
    title="Day 5 Response And Exception Demo",
    description="用于学习统一响应结构、全局异常处理、Swagger 文档和状态码规范。",
    version="0.1.0",
)


@app.exception_handler(AppException)
async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    """统一处理业务异常。"""

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(message=exc.message, code=exc.code),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """统一处理 FastAPI 自带的 HTTPException。"""

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=str(exc.detail),
            code=exc.status_code,
        ),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    """统一处理请求参数校验错误。"""

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            message="请求参数校验失败",
            code=42200,
            data=exc.errors(),
        ),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """兜底异常处理。

    正式项目里通常还会把完整异常写入日志。
    这里先统一成简单可读的响应结构。
    """

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            message="服务器内部错误",
            code=50000,
            data={"error_type": type(exc).__name__},
        ),
    )


app.include_router(users_router)
