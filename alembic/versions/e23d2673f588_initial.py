"""initial

Revision ID: e23d2673f588
Revises:
Create Date: 2026-07-14 17:39:03.501321

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e23d2673f588"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "spimex_trading_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("exchange_product_id", sa.String(length=25), nullable=False),
        sa.Column("exchange_product_name", sa.String(), nullable=False),
        sa.Column("oil_id", sa.String(length=4), nullable=False),
        sa.Column("delivery_basis_id", sa.String(length=3), nullable=False),
        sa.Column("delivery_basis_name", sa.String(length=50), nullable=False),
        sa.Column("delivery_type_id", sa.String(length=1), nullable=False),
        sa.Column("volume", sa.Integer(), nullable=False),
        sa.Column("total", sa.Numeric(precision=16, scale=2), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=False),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("spimex_trading_results")
