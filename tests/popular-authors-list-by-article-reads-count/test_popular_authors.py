import pytest
from rest_framework import status


@pytest.fixture()
@pytest.mark.order(1)
def popular_authors_data(user_factory):
    """
    Fixture to provide data for popular authors tests.
    """

    from tests.factories.article_factory import ArticleFactory

    users = [user_factory.create(is_active=True) for _ in range(5)]

    for user in users:
        articles = ArticleFactory.create_batch(3, author=user)
        for article in articles:
            article.reads_count = 10
            article.save()

    return users


@pytest.mark.django_db
@pytest.mark.order(2)
def test_popular_authors_list(popular_authors_data, api_client, tokens):
    """
    Test fetching the popular authors list.
    """
    user = popular_authors_data[0]
    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.get('/api/users/articles/popular/')

    assert response.status_code == status.HTTP_200_OK

    data = response.json()

    assert 'results' in data
    assert len(data['results']) <= 5

    sorted_users = sorted(
        popular_authors_data,
        key=lambda u: sum(article.reads_count for article in u.article_set.filter(status='publish')),
        reverse=True
    )

    for i in range(len(data['results']) - 1):
        current_user = next((user for user in sorted_users if user.id == data['results'][i]['id']), None)
        next_user = next((user for user in sorted_users if user.id == data['results'][i + 1]['id']), None)

        current_total_reads = sum(article.reads_count for article in current_user.article_set.filter(status='publish')) if current_user else 0
        next_total_reads = sum(article.reads_count for article in next_user.article_set.filter(status='publish')) if next_user else 0

        assert current_total_reads >= next_total_reads


@pytest.mark.django_db
@pytest.mark.order(3)
def test_popular_authors_list_no_authors(api_client, user_factory, tokens):
    """
    Test when there are no active users with published articles.
    """
    user = user_factory.create()
    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.get('/api/users/articles/popular/')

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {'count': 0, 'next': None, 'previous': None, 'results': []}


@pytest.mark.django_db
@pytest.mark.order(4)
def test_popular_authors_list_unauthorized(api_client):
    """
    Test unauthorized access to the popular authors list.
    """

    client = api_client(token='access')
    response = client.get('/api/users/articles/popular/')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
