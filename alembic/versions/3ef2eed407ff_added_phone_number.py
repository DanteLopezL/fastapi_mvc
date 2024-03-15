"""Added phone number

Revision ID: 3ef2eed407ff
Revises: d3ff55000893
Create Date: 2024-03-14 21:54:15.377045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ef2eed407ff'
down_revision: Union[str, None] = 'd3ff55000893'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String() , nullable=True))


def downgrade() -> None:
    pass
