"""Added is Finished in Course table

Revision ID: e19abff4134d
Revises: fcc128219691
Create Date: 2025-06-09 19:32:42.324763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e19abff4134d'
down_revision: Union[str, None] = 'fcc128219691'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courses', sa.Column('isFinished', sa.Boolean(), nullable=True))
    op.alter_column('lessons', 'duration',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('lessons', 'duration',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.drop_column('courses', 'isFinished')
    # ### end Alembic commands ###
