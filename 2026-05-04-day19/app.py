"""Day 19: 错误处理、错误码和中间件示例。"""

import time
from uuid import uuid4

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class BusinessError(Exception):
    def __init__(self, message: str, code: int, status_code: int) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


app = FastAPI(
    title="Day 19 Error And Middleware Demo",
    description="用于学习错误码设计、异常处理和请求中间件。",
    version="0.1.0",
)


@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    request_id = uuid4().hex
    start = time.perf_counter()

    response = await call_next(request)

    cost_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Request-Id"] = request_id
    response.headers["X-Process-Time-Ms"] = f"{cost_ms:.2f}"
    return response


@app.exception_handler(BusinessError)
async def business_error_handler(_: Request, exc: BusinessError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message, "data": None},
    )


@app.exception_handler(Exception)
async def server_error_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 50000,
            "message": "服务器内部错误",
            "data": {"error_type": type(exc).__name__},
        },
    )


@app.get("/demo/business-error")
def demo_business_error() -> dict[str, object]:
    raise BusinessError(message="演示业务异常", code=40001, status_code=status.HTTP_400_BAD_REQUEST)


@app.get("/demo/server-error")
def demo_server_error() -> dict[str, object]:
    raise RuntimeError("演示服务器错误")


@app.get("/demo/ping")
def demo_ping() -> dict[str, object]:
    return {"message": "pong"}
