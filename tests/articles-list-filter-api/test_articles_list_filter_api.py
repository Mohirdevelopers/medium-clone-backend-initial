import pytest
import importlib.util
from django.contrib.auth import get_user_model
from rest_framework import status
from faker import Faker

fake = Faker()

User = get_user_model()


@pytest.mark.order(1)
def test_django_filter_via_importlib():
    """
    The function tests that the django_filters is imported.
    """

    loader = importlib.util.find_spec('django_filters')
    assert loader is not None, "django_filters is not installed"


@pytest.mark.order(2)
def test_articles_list_serializer_create():
    """
    The function tests the serializer of articles list.
    """

    from articles.serializers import ArticleListSerializer

    assert ArticleListSerializer, "ArticleListSerializer not created"


@pytest.mark.order(3)
def test_articles_filterset_class_create():
    """
    The function tests the filterset class of articles list.
    """

    from articles.filters import ArticleFilter

    assert ArticleFilter, "ArticleFilter not created"


@pytest.mark.order(4)
def test_comment_model_created():
    """
    The function tests that the comment model is created.
    """

    from articles.models import Comment
    assert Comment._meta.db_table == "comment", "Comment model not created"
    assert Comment._meta.verbose_name == "Comment", "Comment model not created"
    assert Comment._meta.verbose_name_plural == "Comments", "Comment model not created"
    assert Comment._meta.ordering == ["-created_at"], "Comment model not created"


@pytest.fixture
@pytest.mark.order(5)
def articles_data(user_factory):
    """
    The function create articles data for testing.
    """

    from tests.factories.article_factory import ArticleFactory
    from tests.factories.topic_factory import TopicFactory

    topics = TopicFactory.create_batch(3)
    user = user_factory.create()
    articles = ArticleFactory.create_batch(5, author=user)

    for article in articles:
        article.topics.add(topics[0])
        article.topics.add(topics[1])
        article.topics.add(topics[2])

    return articles, topics, user


@pytest.mark.django_db
@pytest.mark.order(6)
def test_articles(articles_data, api_client, tokens):
    """
    The function tests the articles.
    """

    articles, _, user = articles_data
    access, _ = tokens(user)

    client = api_client(token=access)
    response = client.get('/api/articles/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 5


@pytest.mark.django_db
@pytest.mark.order(7)
def test_articles_top(articles_data, api_client, tokens):
    """
    The function tests the association between articles and topics.
    """

    articles, _, user = articles_data

    articles[3].views_count = 13
    articles[3].save()
    article_0_id = articles[3].id

    articles[4].views_count = 12
    articles[4].save()
    article_1_id = articles[4].id

    access, _ = tokens(user)

    response = api_client(token=access).get('/api/articles/?get_top_articles=2')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['id'] == article_0_id
    assert response.data['results'][1]['id'] == article_1_id

    response1 = api_client(token=access).get('/api/articles/?get_top_articles=None')
    assert response1.status_code == status.HTTP_400_BAD_REQUEST
    assert response1.data['get_top_articles'][0] == 'Enter a number.'


@pytest.mark.django_db
@pytest.mark.order(8)
def test_articles_topic_id(articles_data, api_client, tokens):
    """
    The function tests the association between articles and topics.
    """

    articles, topics, user = articles_data
    access, _ = tokens(user)

    topic_id = topics[0].id
    response = api_client(token=access).get(f'/api/articles/?topic_id={topic_id}')
    assert response.status_code == status.HTTP_200_OK
