from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.utils import verify_password


async def test_register_succeeds_given_valid_data(db_session: AsyncSession, async_client: AsyncClient):
    url = "/register/"
    payload = {
        "email": "example@gmail.com",
        "username": "test_username",
        "password": "test_password",
        "first_name": "John",
        "last_name": "Doe",
    }
    response = await async_client.post(url, json=payload)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "User has been successfully created"

    # confirm changes in db
    statement = select(User).where(User.email == "example@gmail.com")
    result = await db_session.execute(statement)

    user: User = result.scalar_one_or_none()

    assert user is not None
    assert user.username == "test_username"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "example@gmail.com"
    assert verify_password("test_password", user.password) is True
