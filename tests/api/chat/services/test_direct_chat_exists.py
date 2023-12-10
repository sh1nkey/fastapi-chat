from sqlalchemy.ext.asyncio import AsyncSession

from src.api.chat.services import direct_chat_exists
from src.models import Chat, User


async def test_direct_chat_exists_returns_true_given_chat_exists(
    db_session: AsyncSession,
    bob_doug_chat: Chat,
    bob_emily_chat: Chat,
    bob_user: User,
    emily_user: User,
):
    chat_exists = await direct_chat_exists(db_session, current_user=bob_user, recipient_user=emily_user)

    assert chat_exists is True


async def test_direct_chat_exists_returns_false_given_chat_does_not_exist(
    db_session: AsyncSession,
    bob_doug_chat: Chat,
    bob_user: User,
    emily_user: User,
):
    chat_exists = await direct_chat_exists(db_session, current_user=bob_user, recipient_user=emily_user)

    assert chat_exists is False
