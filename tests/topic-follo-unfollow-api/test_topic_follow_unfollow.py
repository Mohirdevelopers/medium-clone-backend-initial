import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from faker import Faker

fake = Faker()
User = get_user_model()


@pytest.mark.order(1)
def test_topic_follow_model_created():
    """
    Test TopicFollow model creation.
    """
    from articles.models import TopicFollow
    assert TopicFollow, "TopicFollow model not created"


@pytest.mark.order(2)
def test_topic_follow_view_created():
    """
    Test TopicFollowView creation.
    """
    from articles.views import TopicFollowView
    assert TopicFollowView, "TopicFollowView not created"


@pytest.fixture()
@pytest.mark.order(3)
def topic_follow_data(request, user_factory):
    """
    Fixture to provide data for follow/unfollow topic tests.
    """
    from tests.factories.topic_factory import TopicFactory

    user = user_factory.create()
    topic = TopicFactory.create()

    def valid_data():
        return 201, topic.id, user

    def non_existent_topic():
        return 404, 999, user

    def unauthorized_user():
        return 401, topic.id, user_factory.create(is_active=False)

    data = {
        "valid_data": valid_data,
        "non_existent_topic": non_existent_topic,
        "unauthorized_user": unauthorized_user
    }

    return data[request.param]()


@pytest.mark.django_db
@pytest.mark.order(4)
@pytest.mark.parametrize(
    'topic_follow_data',
    [
        "valid_data",
        "non_existent_topic",
        "unauthorized_user"
    ],
    indirect=True
)
def test_follow_and_unfollow_topic(topic_follow_data, api_client, tokens):
    """
    Test following and unfollowing a topic.
    """
    status_code, topic_id, user = topic_follow_data

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.post(f'/api/articles/topics/{topic_id}/follow/')
    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        response = client.post(f'/api/articles/topics/{topic_id}/follow/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['detail'].startswith("Siz allaqachon")

        response = client.delete(f'/api/articles/topics/{topic_id}/follow/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = client.delete(f'/api/articles/topics/{topic_id}/follow/')
        assert response.status_code == status.HTTP_404_NOT_FOUND
