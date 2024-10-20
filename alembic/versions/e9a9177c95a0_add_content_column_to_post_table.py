"""add content column to post table


Revision ID: e9a9177c95a0
Revises: 23c869d9c6c4
Create Date: 2024-10-20 16:29:07.368230

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e9a9177c95a0"
down_revision: Union[str, None] = "23c869d9c6c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
