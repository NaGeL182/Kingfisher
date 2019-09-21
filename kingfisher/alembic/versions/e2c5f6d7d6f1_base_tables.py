"""base tables

Revision ID: e2c5f6d7d6f1
Revises: 
Create Date: 2019-09-21 17:47:34.576965

"""
from alembic import op
from sqlalchemy import Column, Integer, String, Boolean


# revision identifiers, used by Alembic.
revision = 'e2c5f6d7d6f1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'configs',
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('value', String)
    )
    op.create_table(
        'extensions',
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('enabled', Boolean)
    )


def downgrade():
    pass
