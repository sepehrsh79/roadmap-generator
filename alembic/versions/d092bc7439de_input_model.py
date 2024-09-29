"""input model

Revision ID: d092bc7439de
Revises: e8f17ffb729b
Create Date: 2024-09-29 15:24:58.842708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd092bc7439de'
down_revision: Union[str, None] = 'e8f17ffb729b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inputs',
    sa.Column('domain', sa.Enum('backend_development', 'frontend_development', 'data_science', 'machine_learning', 'artificial_intelligence', 'ui_ux', 'ios_development', 'android_development', 'hardware_programming', 'blockchain', 'game_development', 'dev_ops', 'cybersecurity_development', 'others', name='domainenum'), nullable=False),
    sa.Column('specific_field', sa.String(), nullable=True),
    sa.Column('level', sa.Enum('absolute_beginner', 'beginner', 'intermediate', 'advanced', name='levelenum'), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('goal', sa.String(), nullable=True),
    sa.Column('learnig_style', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('cost_type', sa.Enum('free', 'paid', 'both', name='costtypeenum'), nullable=False),
    sa.Column('need_certificate', sa.Boolean(), nullable=False),
    sa.Column('learning_language', sa.String(), nullable=False),
    sa.Column('join_community', sa.Boolean(), nullable=False),
    sa.Column('time_commitment', sa.Enum('less_than_5', '_5_10', '_10_20', 'more_than_20', name='timecommitmentenum'), nullable=False),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inputs_id'), 'inputs', ['id'], unique=True)
    op.add_column('users', sa.Column('email', sa.String(), nullable=True))
    op.drop_constraint('users_username_key', 'users', type_='unique')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_unique_constraint('users_username_key', 'users', ['username'])
    op.drop_column('users', 'email')
    op.drop_index(op.f('ix_inputs_id'), table_name='inputs')
    op.drop_table('inputs')
    # ### end Alembic commands ###