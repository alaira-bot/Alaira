"""Add prefixes

Revision ID: cee714b63a7e
Revises: c097fdea31a0
Create Date: 2022-01-27 02:46:59.969030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cee714b63a7e"
down_revision = "c097fdea31a0"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "guild_configs",
        sa.Column("guild", sa.Integer, primary_key=True),
        sa.Column("prefix", sa.String, nullable=False, default="!"),
    )


def downgrade():
    op.drop_table("guild_configs")
