"""init migration

Revision ID: 6b5dae2e4e11
Revises:
Create Date: 2024-06-26 23:10:05.282079


"""
# thirdparty
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6b5dae2e4e11"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=False, comment="Player ID"),
        sa.Column("username", sa.String(length=32), unique=True, nullable=False, comment="Username"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("now()"), comment="Created At"),
        sa.Column("updated_at", sa.DateTime(), nullable=True, comment="Updated At"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("players")
