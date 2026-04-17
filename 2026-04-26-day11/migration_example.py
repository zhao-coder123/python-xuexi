"""Day 11 Alembic 迁移脚本示例。

这不是实际 Alembic 自动生成文件，
而是一个便于学习的最小示例。
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260426_create_users_roles"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """升级：创建 roles 和 users 表。"""

    op.create_table(
        "roles",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=50), nullable=False, unique=True),
        sa.Column("description", sa.String(length=255), nullable=True),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("username", sa.String(length=50), nullable=False, unique=True),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role_id", sa.BigInteger(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
    )


def downgrade() -> None:
    """回滚：按依赖关系反向删除表。"""

    op.drop_table("users")
    op.drop_table("roles")
