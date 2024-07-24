import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from faker import Faker

fake = Faker()
User = get_user_model()


@pytest.fixture
def search_by_article_topic_data(user_factory, topic_factory, article_factory):
    """
    Provides test data for searching articles by topic.
    """
    user = user_factory.create()
    topic = topic_factory.create()
    articles = article_factory.create_batch(3, author=user)

    for article in articles:
        article.topics.add(topic)

    return user, {"search": topic.name}


@pytest.fixture
def search_by_article_title_data(user_factory, topic_factory, article_factory):
    """
    Provides test data for searching articles by title, summary, and content.
    """
    user = user_factory.create()
    title = fake.sentence()
    topic = topic_factory.create()
    articles = article_factory.create_batch(3, author=user, title=title)

    for article in articles:
        article.topics.add(topic)

    return user, {"search_title": title}


@pytest.fixture
def search_by_article_summary(user_factory, topic_factory, article_factory):
    """
    Provides test data for searching articles by title, summary, and content.
    """
    user = user_factory.create()
    summary = fake.paragraph()
    topic = topic_factory.create()
    articles = article_factory.create_batch(3, author=user, summary=summary)

    for article in articles:
        article.topics.add(topic)

    return user, {"search": summary}


@pytest.fixture
def search_by_article_content_data(user_factory, topic_factory, article_factory):
    """
    Provides test data for searching articles by title, summary, and content.
    """
    user = user_factory.create()
    content = fake.text()
    topic = topic_factory.create()
    articles = article_factory.create_batch(3, author=user, content=content)

    for article in articles:
        article.topics.add(topic)

    return user, {"search": content}


@pytest.fixture
def search_by_article_non_existent_data(user_factory, topic_factory, article_factory):
    """
    Provides test data for searching articles with a non-existent search term.
    """
    user = user_factory.create()
    topic = topic_factory.create()
    articles = article_factory.create_batch(3, author=user)

    for article in articles:
        article.topics.add(topic)

    return user, {"search": "non_existent_term"}


@pytest.fixture()
def search_data(request):
    """
    The fixture requests the appropriate search data fixture.
    """
    fixture_name = request.param
    return request.getfixturevalue(fixture_name)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'search_data',
    [
        "search_by_article_topic_data",
        "search_by_article_title_data",
        "search_by_article_summary",
        "search_by_article_content_data",
        "search_by_article_non_existent_data"
    ],
    indirect=True
)
def test_search_articles(search_data, api_client, tokens):
    """
    The function tests the search functionality of articles.
    """
    user, query_params = search_data
    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.get('/articles/search/', data=query_params)

    assert response.status_code == status.HTTP_200_OK

    if query_params.get("search") == "non_existent_term":
        assert len(response.data['results']) == 0
    else:
        assert len(response.data['results']) > 0
