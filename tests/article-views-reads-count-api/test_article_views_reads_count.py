import pytest
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture()
@pytest.mark.order(1)
def article_data(request, user_factory):
    """
    Fixture to provide data for viewing articles.
    """

    from tests.factories.article_factory import ArticleFactory

    user = user_factory.create()
    article = ArticleFactory.create()

    return article.id, user


@pytest.mark.django_db
@pytest.mark.order(2)
def test_increment_reads_count(article_data, api_client, tokens):
    """
    Test incrementing the reads count of an article.
    """

    from articles.models import Article

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
@pytest.mark.order(3)
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


@pytest.mark.order(4)
def test_reading_history_model_exists():
    """
    Test that the ReadingHistory model exists.
    """

    from articles.models import ReadingHistory
    assert ReadingHistory, "ReadingHistory model not created"


@pytest.mark.order(5)
def test_reading_history_serializer_exists():
    """
    Test that the ReadingHistorySerializer exists.
    """

    from articles.serializers import ReadingHistorySerializer
    assert ReadingHistorySerializer, "ReadingHistorySerializer not created"


@pytest.mark.order(6)
def test_reading_history_view_exists():
    """
    Test if reading history view exists.
    """

    from articles.views import ReadingHistoryView
    assert ReadingHistoryView, "ReadingHistoryView not created"


@pytest.mark.django_db
@pytest.mark.order(7)
def test_view_article(article_data, api_client, tokens):
    """
    Test retrieving an article and incrementing the views count.
    """

    from articles.models import Article, ReadingHistory

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
