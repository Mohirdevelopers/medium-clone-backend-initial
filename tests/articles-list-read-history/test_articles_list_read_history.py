import pytest
from rest_framework import status


@pytest.fixture
def articles_user(user_factory, article_factory):
    """
    The function create articles
    """
    user = user_factory.create()
    articles = article_factory.create_batch(5, author=user)

    return articles, user


@pytest.mark.django_db
def test_reading_history_list(api_client, articles_user, tokens):
    """
    Test fetching the reading history list for the user.
    """
    articles, user = articles_user

    access, _ = tokens(user)
    client = api_client(token=access)

    for article in articles:
        client.get(f'/articles/{article.id}/')

    response = client.get('/users/articles/history/')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert len(data['results']) == len(articles)
