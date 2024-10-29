import sqlalchemy as sa

from src.database import metadata

userTable = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("username", sa.String(150), nullable=False, unique=True),
    sa.Column("email", sa.String(150), nullable=False, unique=True),
    sa.Column("password", sa.String(150), nullable=False, unique=False),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), default=sa.func.now()),
)
