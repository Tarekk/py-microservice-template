"""Auto migration

Revision ID: 6f506483a8ac
Revises: 0bdd6c4bf1af
Create Date: 2025-04-06 17:08:03.324824

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '6f506483a8ac'
down_revision = '0bdd6c4bf1af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
