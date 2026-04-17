"""Day 7: Week 1 收口示例入口。"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException
from app.core.response import error_response
from app.routers.users import router as users_router


app = FastAPI(
    title="Day 7 CRUD Demo",
    description="Week 1 收口：一个最小可用的用户 CRUD API。",
    version="0.1.0",
)


@app.exception_handler(AppException)
async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(message=exc.message, code=exc.code),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response(
            message="请求参数校验失败", code=42200, data=exc.errors()
        ),
    )


app.include_router(users_router)
