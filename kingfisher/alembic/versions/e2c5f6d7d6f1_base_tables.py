"""base tables

Revision ID: e2c5f6d7d6f1
Revises: 
Create Date: 2019-09-21 17:47:34.576965

"""
from alembic import op
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, text, ForeignKey


# revision identifiers, used by Alembic.
revision = 'e2c5f6d7d6f1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'config',
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('value', String),
        Column('created_at', DateTime, nullable=False, server_default=func.now()),
        Column('updated_at', DateTime, nullable=True, server_default=text('NULL')),
    )
    op.create_table(
        'extensions',
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('enabled', Boolean),
        Column('created_at', DateTime, nullable=False, server_default=func.now()),
        Column('updated_at', DateTime, nullable=True, server_default=text('NULL')),
    )

    op.create_table(
        'servers',
        Column('id', Integer, primary_key=True),
        Column('sid', Integer, unique=True),
        Column('name', String),
        Column('joined_at', DateTime, nullable=False, server_default=func.now()),
        Column('left_at', DateTime, nullable=True, server_default=text('NULL')),
        Column('created_at', DateTime, nullable=False, server_default=func.now()),
        Column('updated_at', DateTime, nullable=True, server_default=text('NULL')),
    )

    op.create_table(
        'server_flags',
        Column('id', Integer, primary_key=True),
        Column('server_id', Integer, ForeignKey('servers.id')),
        Column('name', String),
        Column('value', String, nullable=True, server_default='NULL'),
        Column('created_at', DateTime, nullable=False, server_default=func.now()),
        Column('updated_at', DateTime, nullable=True, server_default=text('NULL')),
    )


def downgrade():
    pass
