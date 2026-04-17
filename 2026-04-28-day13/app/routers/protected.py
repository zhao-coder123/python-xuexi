"""Day 13 受保护路由。"""

from fastapi import APIRouter, Depends

from app.core.security import get_current_user, require_role


router = APIRouter(tags=["Protected"])


@router.get("/me", summary="获取当前用户")
def read_me(
    current_user: dict[str, object] = Depends(get_current_user),
) -> dict[str, object]:
    return {"message": "success", "data": current_user}


@router.get("/admin/dashboard", summary="管理员接口")
def admin_dashboard(
    current_user: dict[str, object] = Depends(require_role("admin")),
) -> dict[str, object]:
    return {
        "message": "success",
        "data": {"hello": current_user["username"], "scope": "admin"},
    }


@router.get("/editor/articles", summary="编辑接口")
def editor_articles(
    current_user: dict[str, object] = Depends(require_role("editor")),
) -> dict[str, object]:
    return {
        "message": "success",
        "data": {"hello": current_user["username"], "scope": "editor"},
    }
