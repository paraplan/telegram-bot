"""add setting is_notify_vacation

Revision ID: 8cf9b9e9da4b
Revises: 48d3baae21a0
Create Date: 2025-01-27 11:15:48.929586

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8cf9b9e9da4b"
down_revision: Union[str, None] = "48d3baae21a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user_settings",
        sa.Column(
            "is_notify_vacation",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user_settings", "is_notify_vacation")
    # ### end Alembic commands ###
