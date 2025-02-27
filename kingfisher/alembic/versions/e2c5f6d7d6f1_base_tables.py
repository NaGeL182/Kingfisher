"""base tables

Revision ID: e2c5f6d7d6f1
Revises: 
Create Date: 2019-09-21 17:47:34.576965

"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, text, ForeignKey, BigInteger

from alembic import op

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
        Column('sid', BigInteger, unique=True, nullable=False),
        Column('name', String),
        Column('joined_at', DateTime, nullable=False, server_default=func.now()),
        Column('left_at', DateTime, nullable=True, server_default=text('NULL')),
        Column('created_at', DateTime, nullable=False, server_default=func.now()),
        Column('updated_at', DateTime, nullable=True, server_default=text('NULL')),
    )

    op.create_table(
        'server_config',
        Column('id', Integer, primary_key=True),
        Column('server_id', Integer, ForeignKey('servers.id')),
        Column('name', String),
        Column('value', String),
        Column('created_at', DateTime, nullable=False, server_default=func.now()),
        Column('updated_at', DateTime, nullable=True, server_default=text('NULL')),
    )

    op.create_table(
        'roles',
        Column('id', Integer, primary_key=True),
        Column('rid', BigInteger, unique=True, nullable=False),
        Column('name', String),
        Column('server_id', Integer, ForeignKey('servers.id')),
        Column('role_created_at', DateTime, nullable=False),
        Column('role_deleted_at', DateTime, nullable=True, server_default=text('NULL')),
        Column('created_at', DateTime, nullable=False, server_default=func.now()),
        Column('updated_at', DateTime, nullable=True, server_default=text('NULL')),
    )

    op.create_table(
        'users',
        Column('id', Integer, primary_key=True),
        Column('uid', BigInteger, unique=True, nullable=False),
        Column('name', String),
        Column('discriminator', String),
        Column('created_at', DateTime, nullable=False, server_default=func.now()),
        Column('updated_at', DateTime, nullable=True, server_default=text('NULL')),
    )

    op.create_table(
        'members',
        Column('id', Integer, primary_key=True),
        Column('user_id', Integer, ForeignKey('users.id')),
        Column('server_id', Integer, ForeignKey('servers.id')),
        Column('joined_at', DateTime, nullable=False, server_default=func.now()),
        Column('left_at', DateTime, nullable=True, server_default=text('NULL')),
        Column('created_at', DateTime, nullable=False, server_default=func.now()),
        Column('updated_at', DateTime, nullable=True, server_default=text('NULL')),
    )

    op.create_table(
        'member2role',
        Column('member_id', Integer, ForeignKey('members.id')),
        Column('role_id', Integer, ForeignKey('roles.id')),
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

    op.create_table(
        'role_flags',
        Column('id', Integer, primary_key=True),
        Column('role_id', Integer, ForeignKey('roles.id')),
        Column('name', String),
        Column('value', String, nullable=True, server_default='NULL'),
        Column('created_at', DateTime, nullable=False, server_default=func.now()),
        Column('updated_at', DateTime, nullable=True, server_default=text('NULL')),
    )

    op.create_table(
        'member_flags',
        Column('id', Integer, primary_key=True),
        Column('member_id', Integer, ForeignKey('members.id')),
        Column('name', String),
        Column('value', String, nullable=True, server_default='NULL'),
        Column('created_at', DateTime, nullable=False, server_default=func.now()),
        Column('updated_at', DateTime, nullable=True, server_default=text('NULL')),
    )


def downgrade():
    pass
