import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.enums import StatusNotificationEnum, TypeNotificationEnum
from core.database.models import Notification


@pytest.fixture
async def notification_in_db(session: AsyncSession):
    notification = Notification(
        type=TypeNotificationEnum.EMAIL.value,
        recipient="test@example.com",
        subject="Test",
        message_text="Test text"
    )
    session.add(notification)
    await session.commit()
    await session.refresh(notification)
    
    yield notification
    
    await session.delete(notification)
    await session.commit()


def create_notification_request_data(**overrides):
    request_data = {
        "type": "email",
        "recipient": "example@gmail.com",
        "subject": "string",
        "message_text": "string",
        "message_html": "",
        "attachments": []
    }
    request_data.update(overrides)
    return request_data

@pytest.mark.parametrize(
    "request_data, expectation_status_code",
    [
        (create_notification_request_data(), 200),
        (create_notification_request_data(type="sms", recipient="+7949111111"), 200),
        (create_notification_request_data(recipient="234"), 422),
        (create_notification_request_data(type="sms"), 422),
        (create_notification_request_data(type=""), 422),
        (create_notification_request_data(attachments=["file1, file2"]), 400),
        (create_notification_request_data(message_html="hello", type="sms", recipient="+7949111111"), 400),
        (create_notification_request_data(type="sms", recipient="+7949111111", attachments=["file"]), 400),
        (create_notification_request_data(type="sms", recipient="+7949111111", message_text=""), 400),
    ]
    )
async def test_create_notification_handler(
    async_client: AsyncClient,
    request_data,
    expectation_status_code
):
    response = await async_client.post("/notifications/", json=request_data)
    assert response.status_code == expectation_status_code
    if response.status_code == 200:
        data = response.json()
        assert data["type"] == request_data["type"]
        assert data["recipient"] == request_data["recipient"]
        assert data["subject"] == request_data["subject"]
        
async def test_get_notifications_handler(async_client: AsyncClient, notification_in_db):
    query_params = {
        "limit": 1000,
        "offset": 0,
        "type": TypeNotificationEnum.EMAIL.value,
    }
    response = await async_client.get("/notifications/", params=query_params)
    assert response.status_code == 200
    data = response.json()
    if data:
        first_item = data[0]
        assert "id" in first_item
        assert "type" in first_item
        assert "recipient" in first_item
        assert "subject" in first_item
    
async def test_get_notification_handler(async_client: AsyncClient, notification_in_db):
    response = await async_client.get(f"/notifications/{notification_in_db.id}/")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == str(notification_in_db.id)
    assert data["type"] == notification_in_db.type
    assert data["recipient"] == notification_in_db.recipient
    assert data["subject"] == notification_in_db.subject
    assert data["message_text"] == notification_in_db.message_text
    