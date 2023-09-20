from datetime import datetime
from uuid import UUID

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Chat, ChatType, Message, User


async def get_direct_chat(db_session: AsyncSession, *, initiator_user: User, recipient_user: User) -> Chat | None:
    query = (
        select(Chat)
        .where(
            and_(
                Chat.chat_type == ChatType.DIRECT,
                Chat.users.contains(initiator_user),
                Chat.users.contains(recipient_user),
                Chat.is_active.is_(True),
            )
        )
        .options(selectinload(Chat.users))
    )
    result = await db_session.execute(query)
    # sqlalchemy.exc.MultipleResultsFound
    chat: Chat | None = result.scalar_one_or_none()

    return chat


async def create_direct_chat(db_session: AsyncSession, *, initiator_user: User, recipient_user: User) -> Chat:
    chat = Chat(chat_type=ChatType.DIRECT)
    chat.users.append(initiator_user)
    chat.users.append(recipient_user)
    db_session.add(chat)
    await db_session.commit()

    return chat


async def get_chat_by_guid(db_session: AsyncSession, *, chat_guid: UUID) -> Chat | None:
    query = select(Chat).where(Chat.guid == chat_guid).options(selectinload(Chat.messages), selectinload(Chat.users))
    result = await db_session.execute(query)
    chat: Chat | None = result.scalar_one_or_none()

    return chat


async def get_user_by_guid(db_session: AsyncSession, *, user_guid: UUID) -> User | None:
    query = select(User).where(User.guid == user_guid)
    result = await db_session.execute(query)
    user: User | None = result.scalar_one_or_none()

    return user


# TODO: Should I differentiate message sending based on chat type?!
async def send_message_to_chat(db_session: AsyncSession, *, content: str, chat_id: int, user_id: int) -> Message:
    message = Message(content=content, chat_id=chat_id, user_id=user_id)
    db_session.add(message)
    await db_session.commit()

    return message


async def get_user_chats(db_session: AsyncSession, *, current_user: User) -> list[Chat]:
    query = (
        select(Chat)
        .where(
            and_(
                Chat.users.contains(current_user),
            )
        )
        .options(selectinload(Chat.users))
    )
    result = await db_session.execute(query)

    chats: list[Chat] = result.scalars().all()

    return chats


async def get_paginated_chat_messages(db_session: AsyncSession, *, chat_id: int) -> list[Chat]:
    query = (
        select(Message)
        .where(and_(Message.chat_id == chat_id, Message.is_active.is_(True)))
        .order_by(Message.created_at.desc())
        .options(selectinload(Message.user), selectinload(Message.chat))
    )
    return await paginate(db_session, query)


async def get_active_message_by_guid_and_chat(
    db_session: AsyncSession, *, chat_id: int, message_guid: UUID
) -> Message | None:
    query = select(Message).where(
        and_(Message.guid == message_guid, Message.is_active.is_(True), Message.chat_id == chat_id)
    )

    result = await db_session.execute(query)
    message: Message | None = result.scalar_one_or_none()

    return message


async def get_older_chat_messages(
    db_session: AsyncSession,
    *,
    chat_id: int,
    limit: int = 10,
    created_at: datetime,
) -> tuple[list[Message], bool]:
    query = (
        select(Message)
        .where(
            and_(
                Message.chat_id == chat_id,
                Message.is_active.is_(True),
                Message.created_at < created_at,
            )
        )
        .order_by(Message.created_at.desc())
        .limit(limit + 1)  # Fetch limit + 1 messages
        .options(selectinload(Message.user), selectinload(Message.chat))
    )

    result = await db_session.execute(query)
    older_messages: list[Message] = result.scalars().all()

    # Determine if there are more messages
    has_more_messages = len(older_messages) > limit

    # Return the first 'limit' messages and a flag indicating if there are more
    return older_messages[:limit], has_more_messages
