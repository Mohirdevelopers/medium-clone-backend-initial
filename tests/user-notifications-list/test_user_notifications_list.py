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
def notification_data(user_factory):
    """
    Create notification data for testing.
    """

    from tests.factories.notification_factory import NotificationFactory

    user = user_factory.create()
    notifications = NotificationFactory.create_batch(3, user=user, read_at=None)
    return user, notifications


@pytest.mark.django_db
@pytest.mark.parametrize(
    'notification_data',
    [
        ('valid_data',),
    ],
    indirect=True
)
def test_get_all_notifications(notification_data, api_client, tokens):
    """
    Test getting all user notifications.
    """
    user, notifications = notification_data
    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.get('/users/notifications/')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == len(notifications)


@pytest.fixture
def single_notification(user_factory):
    """
    Create a single notification for testing.
    """

    from tests.factories.notification_factory import NotificationFactory

    user = user_factory.create()
    notification = NotificationFactory.create(user=user, read_at=None)
    return user, notification


@pytest.mark.django_db
@pytest.mark.parametrize(
    'single_notification',
    [
        ('valid_data',),
    ],
    indirect=True
)
def test_retrieve_notification(single_notification, api_client, tokens):
    """
    Test retrieving a single notification.
    """
    user, notification = single_notification
    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.get(f'/users/notifications/{notification.id}/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == notification.id

@pytest.mark.django_db
@pytest.mark.parametrize(
    'single_notification',
    [
        ('valid_data',),
    ],
    indirect=True
)
def test_update_notification(single_notification, api_client, tokens):
    """
    Test updating a notification to mark it as read.
    """
    user, notification = single_notification
    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.patch(f'/users/notifications/{notification.id}/')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    notification.refresh_from_db()
    assert notification.read_at is not None

    response = client.get('/users/notifications/')
    notifications = response.data.get('results', [])

    assert all(n['id'] != notification.id for n in notifications)
