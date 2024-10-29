import sqlalchemy as sa

from src.database import metadata

transactionTable = sa.Table(
    "transactions",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("id_account", sa.Integer, sa.ForeignKey("accounts.id"), nullable=False),
    sa.Column("type", sa.String(150), nullable=False),
    sa.Column("amount", sa.Numeric(10, 2), nullable=False),
    sa.Column("timestamp", sa.TIMESTAMP(timezone=True), default=sa.func.now()),
)
