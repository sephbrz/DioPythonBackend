import sqlalchemy as sa

from src.database import metadata

accountTable = sa.Table(
    "accounts",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("id_user", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    sa.Column("balance", sa.Numeric(10, 2), nullable=False, default=0),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), default=sa.func.now()),
)
