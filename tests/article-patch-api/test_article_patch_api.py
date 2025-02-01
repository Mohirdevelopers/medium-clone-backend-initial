import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from faker import Faker

fake = Faker()

User = get_user_model()


@pytest.fixture()
def article_patch_data(request, user_factory):
    """
    Fixture to provide data for PATCH update article tests.
    """

    from tests.factories.topic_factory import TopicFactory
    from tests.factories.article_factory import ArticleFactory

    topic = TopicFactory.create()
    user = user_factory.create()
    article = ArticleFactory.create(author=user)
    article.topics.add(topic.id)
    article.save()

    def valid_patch_data():
        return (
            200, article.id, user, {
                "summary": "this is test updated summary"
            }
        )

    def invalid_patch_data():
        return (
            400, article.id, user, {
                "summary": ""
            }
        )

    def non_existent_article():
        return (
            404, 999, user, {
                "summary": "this is test updated summary"
            }
        )

    data = {
        "valid_patch_data": valid_patch_data,
        "invalid_patch_data": invalid_patch_data,
        "non_existent_article": non_existent_article,
    }

    return data[request.param]()


@pytest.mark.django_db
@pytest.mark.parametrize(
    'article_patch_data',
    [
        "valid_patch_data",
        "invalid_patch_data",
        "non_existent_article",
    ],
    indirect=True
)
def test_article_patch(article_patch_data, api_client, tokens):
    """
    The function tests updating an article with multipart form data.
    """

    status_code, article_id, user, patch_data = article_patch_data

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.patch(f'/api/articles/{article_id}/', data=patch_data, format='multipart')

    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        assert response.data['summary'] == patch_data['summary']
