import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from faker import Faker

fake = Faker()
User = get_user_model()


@pytest.mark.order(1)
def test_search_filter_created():
    """
    Test that the search filter is created.
    """

    from articles.filters import SearchFilter

    assert SearchFilter, "SearchFilter not created"


@pytest.mark.order(2)
def test_search_view_created():
    """
    Test that the search view is created.
    """

    from articles.views import SearchView

    assert SearchView, "SearchView not created"


@pytest.fixture
@pytest.mark.order(3)
def search_by_article_topic_data(user_factory):
    """
    Provides test data for searching articles by topic.
    """

    from tests.factories.topic_factory import TopicFactory
    from tests.factories.article_factory import ArticleFactory

    user = user_factory.create()
    topic = TopicFactory.create()
    articles = ArticleFactory.create_batch(3, author=user)

    for article in articles:
        article.topics.add(topic)

    return user, {"search": topic.name}


@pytest.fixture
@pytest.mark.order(4)
def search_by_article_title_data(user_factory):
    """
    Provides test data for searching articles by title, summary, and content.
    """

    from tests.factories.topic_factory import TopicFactory
    from tests.factories.article_factory import ArticleFactory

    user = user_factory.create()
    title = fake.sentence()
    topic = TopicFactory.create()
    articles = ArticleFactory.create_batch(3, author=user, title=title)

    for article in articles:
        article.topics.add(topic)

    return user, {"search_title": title}


@pytest.fixture
@pytest.mark.order(5)
def search_by_article_summary(user_factory):
    """
    Provides test data for searching articles by title, summary, and content.
    """

    from tests.factories.topic_factory import TopicFactory
    from tests.factories.article_factory import ArticleFactory

    user = user_factory.create()
    summary = fake.paragraph()
    topic = TopicFactory.create()
    articles = ArticleFactory.create_batch(3, author=user, summary=summary)

    for article in articles:
        article.topics.add(topic)

    return user, {"search": summary}


@pytest.fixture
@pytest.mark.order(6)
def search_by_article_content_data(user_factory):
    """
    Provides test data for searching articles by title, summary, and content.
    """

    from tests.factories.topic_factory import TopicFactory
    from tests.factories.article_factory import ArticleFactory

    user = user_factory.create()
    content = fake.text()
    topic = TopicFactory.create()
    articles = ArticleFactory.create_batch(3, author=user, content=content)

    for article in articles:
        article.topics.add(topic)

    return user, {"search": content}


@pytest.fixture
@pytest.mark.order(7)
def search_by_article_non_existent_data(user_factory):
    """
    Provides test data for searching articles with a non-existent search term.
    """

    from tests.factories.topic_factory import TopicFactory
    from tests.factories.article_factory import ArticleFactory

    user = user_factory.create()
    topic = TopicFactory.create()
    articles = ArticleFactory.create_batch(3, author=user)

    for article in articles:
        article.topics.add(topic)

    return user, {"search": "non_existent_term"}


@pytest.fixture()
@pytest.mark.order(8)
def search_data(request):
    """
    The fixture requests the appropriate search data fixture.
    """
    fixture_name = request.param
    return request.getfixturevalue(fixture_name)


@pytest.mark.django_db
@pytest.mark.order(9)
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
