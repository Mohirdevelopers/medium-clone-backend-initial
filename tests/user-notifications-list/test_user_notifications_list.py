import pytest
from rest_framework import status


@pytest.mark.order(1)
def test_notification_model_exists():
    """
    Test Notification model exists.
    """
    from users.models import Notification
    assert Notification, "Notification model not created"


@pytest.fixture
def notification_data_factory(user_factory, request):
    """
    Create notification data for testing.
    """
    from tests.factories.notification_factory import NotificationFactory

    user = user_factory.create()
    if request.param == "multiple":
        notifications = NotificationFactory.create_batch(3, user=user, read_at=None)
    else:
        notifications = [NotificationFactory.create(user=user, read_at=None)]
    return user, notifications


@pytest.mark.django_db
@pytest.mark.parametrize(
    'notification_data_factory',
    [
        "multiple",
        "single"
    ],
    indirect=True
)
def test_notifications(notification_data_factory, api_client, tokens):
    """
    Test notification endpoints.
    """
    user, notifications = notification_data_factory
    access, _ = tokens(user)
    client = api_client(token=access)

    # Test getting all notifications
    response = client.get('/api/users/notifications/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == len(notifications)

    if len(notifications) == 1:
        notification = notifications[0]

        # Test retrieving a single notification
        response = client.get(f'/api/users/notifications/{notification.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == notification.id

        # Test updating a notification to mark it as read
        response = client.patch(f'/api/users/notifications/{notification.id}/', data={'read': True})
        assert response.status_code == status.HTTP_204_NO_CONTENT

        notification.refresh_from_db()
        assert notification.read_at is not None

        response = client.get('/api/users/notifications/')
        notifications = response.data.get('results', [])
        assert all(n['id'] != notification.id for n in notifications)
