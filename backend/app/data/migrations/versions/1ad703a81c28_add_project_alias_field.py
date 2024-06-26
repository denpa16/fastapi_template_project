"""add project alias field

Revision ID: 1ad703a81c28
Revises: 4963ae24edbe
Create Date: 2024-04-06 13:26:06.207730

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1ad703a81c28"
down_revision: Union[str, None] = "4963ae24edbe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("projects", sa.Column("alias", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("projects", "alias")
    # ### end Alembic commands ###
