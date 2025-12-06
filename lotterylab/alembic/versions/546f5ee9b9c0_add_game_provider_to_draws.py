"""add game_provider to draws

Revision ID: 546f5ee9b9c0
Revises: cf7c749d01a2
Create Date: 2025-09-08 11:28:38.072970

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '546f5ee9b9c0'
down_revision: Union[str, None] = 'cf7c749d01a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    cols = {c['name'] for c in inspector.get_columns('draws')}
    if 'game_provider' not in cols:
        op.add_column('draws', sa.Column('game_provider', sa.String(length=50), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    cols = {c['name'] for c in inspector.get_columns('draws')}
    if 'game_provider' in cols:
        op.drop_column('draws', 'game_provider')
