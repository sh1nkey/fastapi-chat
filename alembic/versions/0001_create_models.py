"""create models

Revision ID: 0001
Revises:
Create Date: 2023-09-11 17:34:46.924046

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "chat",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("guid", sa.UUID(), nullable=False),
        sa.Column(
            "chat_type", sa.Enum("DIRECT", "GROUP", name="chattype", schema="chat", inherit_schema=True), nullable=False
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="chat",
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("guid", sa.UUID(), nullable=False),
        sa.Column("password", sa.String(length=128), nullable=False),
        sa.Column("username", sa.String(length=150), nullable=False),
        sa.Column("first_name", sa.String(length=150), nullable=False),
        sa.Column("last_name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("last_login", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("guid"),
        sa.UniqueConstraint("username"),
        schema="chat",
    )
    op.create_table(
        "chat_participant",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["chat_id"],
            ["chat.chat.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["chat.user.id"],
        ),
        sa.PrimaryKeyConstraint("user_id", "chat_id"),
        schema="chat",
    )
    op.create_table(
        "message",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("guid", sa.UUID(), nullable=False),
        sa.Column("content", sa.String(length=5000), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["chat_id"],
            ["chat.chat.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["chat.user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="chat",
    )
    op.create_table(
        "read_status",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("last_read_message_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["chat_id"],
            ["chat.chat.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["chat.user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="chat",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("read_status", schema="chat")
    op.drop_table("message", schema="chat")
    op.drop_table("chat_participant", schema="chat")
    op.drop_table("user", schema="chat")
    op.drop_table("chat", schema="chat")
    sa.Enum("DIRECT", "GROUP", name="chattype", schema="chat", inherit_schema=True).drop(op.get_bind())
    # ### end Alembic commands ###
