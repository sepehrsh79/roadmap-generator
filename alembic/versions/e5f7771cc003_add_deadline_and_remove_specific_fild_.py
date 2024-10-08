"""add deadline and remove specific_fild from Input

Revision ID: e5f7771cc003
Revises: d092bc7439de
Create Date: 2024-09-29 16:05:42.511895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e5f7771cc003'
down_revision: Union[str, None] = 'd092bc7439de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inputs', sa.Column('deadline', sa.Integer(), nullable=False))
    op.alter_column('inputs', 'learnig_style',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=False)
    op.drop_column('inputs', 'specific_field')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('inputs', sa.Column('specific_field', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.alter_column('inputs', 'learnig_style',
               existing_type=postgresql.ARRAY(sa.VARCHAR()),
               nullable=True)
    op.drop_column('inputs', 'deadline')
    # ### end Alembic commands ###
