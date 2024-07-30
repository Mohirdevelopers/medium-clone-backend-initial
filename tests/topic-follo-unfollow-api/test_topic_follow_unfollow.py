import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from faker import Faker

fake = Faker()

User = get_user_model()


@pytest.mark.order(1)
def test_topic_follow_view_created():
    """
    The function tests topic follow view created.
    """

    from articles.views import TopicFollowView

    assert TopicFollowView, "TopicFollowView not created"


@pytest.fixture()
@pytest.mark.order(2)
def follow_to_topic_data(request, user_factory):
    """
    Fixture to provide data for follow to topic tests.
    """

    from tests.factories.topic_factory import TopicFactory

    user = user_factory.create()
    topic = TopicFactory.create()

    def valid_follow_data():
        return (
            201, topic.id, user
        )

    def non_existent_topic():
        return (
            404, 999, user
        )

    def unauthorized_user():
        return (
            401, topic.id, user_factory.create(is_active=False)
        )

    data = {
        "valid_follow_data": valid_follow_data,
        "non_existent_topic": non_existent_topic,
        "unauthorized_user": unauthorized_user
    }

    return data[request.param]()

@pytest.mark.django_db
@pytest.mark.order(3)
@pytest.mark.parametrize(
    'follow_to_topic_data',
    [
        "valid_follow_data",
        "non_existent_topic",
        "unauthorized_user"
    ],
    indirect=True
)
def test_follow_to_topic(follow_to_topic_data, api_client, tokens):
    """
    The function tests following a topic.
    """
    status_code, topic_id, user = follow_to_topic_data

    access, _ = tokens(user)
    client = api_client(token=access)
    response = client.post(f'/articles/topics/{topic_id}/follow/')

    assert response.status_code == status_code
    if status_code == status.HTTP_201_CREATED:
        response = client.post(f'/articles/topics/{topic_id}/follow/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['detail'].startswith("Siz allaqachon")


@pytest.fixture()
def unfollow_to_topic_data(request, user_factory):
    """
    Fixture to provide data for unfollow to topic tests.
    """

    from tests.factories.topic_factory import TopicFactory

    user = user_factory.create()
    topic = TopicFactory.create()

    def valid_unfollow_data():
        return (
            201, topic.id, user
        )

    def non_existent_topic():
        return (
            404, 999, user
        )

    def unauthorized_user():
        return (
            401, topic.id, user_factory.create(is_active=False)
        )

    data = {
        "valid_unfollow_data": valid_unfollow_data,
        "non_existent_topic": non_existent_topic,
        "unauthorized_user": unauthorized_user
    }

    return data[request.param]()

@pytest.mark.django_db
@pytest.mark.parametrize(
    'unfollow_to_topic_data',
    [
        "valid_unfollow_data",
        "non_existent_topic",
        "unauthorized_user"
    ],
    indirect=True
)
def test_unfollow_to_topic(unfollow_to_topic_data, api_client, tokens):
    """
    The function tests unfollowing a topic.
    """
    status_code, topic_id, user = unfollow_to_topic_data

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.post(f'/articles/topics/{topic_id}/follow/')

    assert response.status_code == status_code

    if response.status_code == status.HTTP_201_CREATED:
        response = client.delete(f'/articles/topics/{topic_id}/follow/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = client.delete(f'/articles/topics/{topic_id}/follow/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
