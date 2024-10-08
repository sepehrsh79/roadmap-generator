"""remove description from LearningDay

Revision ID: bb0e157c6c24
Revises: 1c665cbbbd5f
Create Date: 2024-10-02 01:40:19.615390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb0e157c6c24'
down_revision: Union[str, None] = '1c665cbbbd5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('learning_days', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('learning_days', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
