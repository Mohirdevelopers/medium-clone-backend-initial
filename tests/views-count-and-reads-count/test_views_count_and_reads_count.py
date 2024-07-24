import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from articles.models import Article, ReadingHistory

User = get_user_model()


@pytest.fixture()
def article_data(request, user_factory, article_factory):
    """
    Fixture to provide data for viewing articles.
    """
    user = user_factory.create()
    article = article_factory.create()

    return article.id, user


@pytest.mark.django_db
def test_view_article(article_data, api_client, tokens):
    """
    Test retrieving an article and incrementing the views count.
    """
    article_id, user = article_data

    access, _ = tokens(user)
    client = api_client(token=access)

    article = Article.objects.get(id=article_id)
    initial_views_count = article.views_count

    response = client.get(f'/articles/{article_id}/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == article_id

    article.refresh_from_db()
    assert article.views_count == initial_views_count + 1

    assert ReadingHistory.objects.filter(user=user, article=article).exists()


@pytest.mark.django_db
def test_increment_reads_count(article_data, api_client, tokens):
    """
    Test incrementing the reads count of an article.
    """
    article_id, user = article_data

    access, _ = tokens(user)
    client = api_client(token=access)

    article = Article.objects.get(id=article_id)
    initial_reads_count = article.reads_count

    response = client.post(f'/articles/{article_id}/read/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['detail'] == "Maqolani o'qish soni ortdi."

    article.refresh_from_db()
    assert article.reads_count == initial_reads_count + 1

    response = client.post(f'/articles/{article_id}/read/')
    assert response.status_code == status.HTTP_200_OK
    article.refresh_from_db()
    assert article.reads_count == initial_reads_count + 2


@pytest.mark.django_db
def test_increment_reads_count_article_not_found(article_data, api_client, tokens):
    """
    Test incrementing reads count for a non-existent article.
    """
    _, user = article_data

    access, _ = tokens(user)
    client = api_client(token=access)

    non_existent_article_id = 99999007654
    response = client.post(f'/articles/{non_existent_article_id}/read/')

    assert response.status_code == status.HTTP_404_NOT_FOUND
