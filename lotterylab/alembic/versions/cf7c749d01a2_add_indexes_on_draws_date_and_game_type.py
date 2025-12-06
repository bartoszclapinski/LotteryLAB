"""add indexes on draws date and game_type

Revision ID: cf7c749d01a2
Revises: 34d63ce4d3a7
Create Date: 2025-09-06 16:34:20.770524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf7c749d01a2'
down_revision: Union[str, None] = '34d63ce4d3a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('idx_draws_date', 'draws', ['draw_date'], unique=False)
    op.create_index('idx_draws_game_type', 'draws', ['game_type'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_draws_game_type', table_name='draws')
    op.drop_index('idx_draws_date', table_name='draws')
