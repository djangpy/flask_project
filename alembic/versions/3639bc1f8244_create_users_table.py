"""Create users table

Revision ID: 3639bc1f8244
Revises: 
Create Date: 2019-04-27 15:50:54.603001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3639bc1f8244'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String),
        sa.Column("password", sa.String)
    )


def downgrade():
    op.drop_table("user")
