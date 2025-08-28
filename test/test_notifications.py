import pytest
from httpx import AsyncClient


def create_notification_request_data(**overrides):
    request_data = {
        "type": "email",
        "recipient": "example@gmail.com",
        "subject": "string",
        "message_text": "string",
        "message_html": "",
        "attachments": [
        "string1","string2"
        ]
    }
    request_data.update(overrides)
    return request_data

@pytest.mark.parametrize(
    "request_data, expectation_status_code",
    [
        (create_notification_request_data(), 200),
        (create_notification_request_data(recipient="234"), 422),
        (create_notification_request_data(type="sms"), 422),
        (create_notification_request_data(type=""), 422),
    ]
    )
async def test_create_notification_handler(
    async_client: AsyncClient,
    request_data,
    expectation_status_code
    ):
    response = await async_client.post("/notifications/", json=request_data)
    assert response.status_code == expectation_status_code
    