"""create user table

Revision ID: e800b8ed3d57
Revises: 
Create Date: 2023-10-19 17:10:52.709319

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e800b8ed3d57'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('userID', sa.Integer, primary_key=True),
        sa.Column('userName', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('birthday', sa.Date),
        sa.Column('create_time', sa.DateTime),
        sa.Column('last_login', sa.DateTime)
    )


def downgrade():
    op.drop_table('user')