"""Changed the duration column to integer

Revision ID: 41635839182b
Revises: e19abff4134d
Create Date: 2025-06-09 20:26:49.681681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41635839182b'
down_revision: Union[str, None] = 'e19abff4134d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("ALTER TABLE lessons ALTER COLUMN duration TYPE INTEGER USING duration::integer")

    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('lessons', 'duration',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    # ### end Alembic commands ###
 