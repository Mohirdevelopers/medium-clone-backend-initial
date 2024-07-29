import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from faker import Faker
from django.conf import settings

fake = Faker()

User = get_user_model()


@pytest.mark.order(1)
def test_articles_app_created():
    """
    The function tests that the articles app is created.
    """
    assert "articles" in settings.INSTALLED_APPS, "articles app not installed"


@pytest.mark.order(2)
def test_articles_app_exists():
    """
    The function tests that the articles app exists.
    """

    app_name = 'articles'

    try:
        import articles  # noqa
    except ImportError:
        assert False, f"{app_name} app folder missing"
    assert app_name in settings.INSTALLED_APPS, f"{app_name} app not installed"


@pytest.mark.order(3)
def test_articles_model_created():
    """
    The function tests that the articles model is created.
    """
    from articles.models import Article
    assert Article._meta.db_table == "article"
    assert Article._meta.verbose_name == "Article"
    assert Article._meta.verbose_name_plural == "Articles"
    assert Article._meta.ordering == ["-created_at"]


@pytest.mark.order(4)
def test_topics_model_created():
    """
    The function tests that the topics model is created.
    """
    from articles.models import Topic
    assert Topic._meta.db_table == "topic"
    assert Topic._meta.verbose_name == "Topic"
    assert Topic._meta.verbose_name_plural == "Topics"
    assert Topic._meta.ordering == ["name"]


@pytest.fixture()
@pytest.mark.order(5)
def test_article_create_data(request, user_factory, topic_factory):
    """
    The function creates articles data for testing.
    """

    topic = topic_factory.create_batch(2)
    user = user_factory.create()

    def valid_data():
        return (
            201, user, {
                "title": "first article",
                "summary": "first article summary",
                "content": "first article content",
                "topics": topic[0].id
            }
        )

    def invalid_data():
        return (
            400, user, {
                "title": "",
                "summary": "",
                "content": "",
                "topics": ""
            }
        )

    def empty_article_title():
        return (
            400, user, {
                "title": "",
                "summary": "first article summary",
                "content": "first article content",
                "topics": topic[0].id
            }
        )

    def empty_article_summary():
        return (
            400, user, {
                "title": "first article",
                "summary": "",
                "content": "first article content",
                "topics": topic[0].id
            }
        )

    def required_topic():
        return (
            400, user, {
                "title": "first article",
                "summary": "first article summary",
                "content": "first article content",
                "topics": ''
            }
        )

    data = {
        "valid_data": valid_data,
        "invalid_data": invalid_data,
        "empty_article_title": empty_article_title,
        "empty_article_summary": empty_article_summary,
        "required_topic": required_topic,
    }

    return data[request.param]()


@pytest.mark.order(6)
@pytest.mark.django_db
@pytest.mark.parametrize(
    'test_article_create_data',
    [
        "valid_data",
        "invalid_data",
        "empty_article_title",
        "empty_article_summary",
        "required_topic"
    ],
    indirect=True
)
def test_article_create(test_article_create_data, api_client, tokens):
    """
    The function tests article creation with multipart form data.
    """

    status_code, user, data = test_article_create_data
    access, _ = tokens(user)
    client = api_client(token=access)

    data = {
        "title": data.get('title'),
        "summary": data.get('summary'),
        "content": data.get('content'),
        "topic_ids": data.get('topics')
    }

    response = client.post('/articles/', data=data, format='multipart')

    assert response.status_code == status_code

    if status_code == 201:
        assert response.status_code == status_code
        assert response.data['title'] == data['title']
        assert response.data['summary'] == data['summary']
        assert response.data['content'] == data['content']
        assert len(response.data['topics']) == 1


@pytest.fixture()
@pytest.mark.order(7)
def article_retrieve_data(request, topic_factory, article_factory, user_factory):
    """
    The function creates data for testing article retrieval.
    """

    topic = topic_factory.create()
    user = user_factory.create()
    article = article_factory.create(author=user)
    article.topics.add(topic.id)
    article.save()

    def valid_data():
        return (
            200, article.id, user
        )

    def invalid_data():
        return (
            404, 999, user
        )

    def required_id():
        return (
            404, None, user
        )

    data = {
        "valid_data": valid_data,
        "invalid_data": invalid_data,
        "required_id": required_id
    }

    return data[request.param]()


@pytest.mark.order(8)
@pytest.mark.django_db
@pytest.mark.parametrize(
    'article_retrieve_data',
    [
        "valid_data",
        "invalid_data",
        "required_id",
    ],
    indirect=True
)
def test_article_retrieve(article_retrieve_data, api_client, tokens):
    """
    The function tests article retrieval with multipart form data.
    """

    status_code, article_id, user = article_retrieve_data

    access, _ = tokens(user)
    client = api_client(token=access)
    response = client.get(f'/articles/{article_id}/')

    assert response.status_code == status_code

    if response.status_code == status.HTTP_200_OK:
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == article_id
