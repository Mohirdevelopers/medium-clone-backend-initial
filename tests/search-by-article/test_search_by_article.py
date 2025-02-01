import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from faker import Faker

fake = Faker()
User = get_user_model()

@pytest.fixture
def search_data_factory(user_factory, request):
    """
    Provides test data for searching articles by various criteria.
    """
    from tests.factories.topic_factory import TopicFactory
    from tests.factories.article_factory import ArticleFactory

    user = user_factory.create()
    topic = TopicFactory.create()
    search_type = request.param

    if search_type == "by_topic":
        articles = ArticleFactory.create_batch(3, author=user)
        for article in articles:
            article.topics.add(topic)
        return user, {"search": topic.name}, [article.id for article in articles]

    elif search_type == "by_title":
        title = fake.sentence()
        articles = ArticleFactory.create_batch(3, author=user, title=title)
        for article in articles:
            article.topics.add(topic)
        return user, {"search": title}, [article.id for article in articles]

    elif search_type == "by_summary":
        summary = fake.paragraph()
        articles = ArticleFactory.create_batch(3, author=user, summary=summary)
        for article in articles:
            article.topics.add(topic)
        return user, {"search": summary}, [article.id for article in articles]

    elif search_type == "by_content":
        content = fake.text()
        articles = ArticleFactory.create_batch(3, author=user, content=content)
        for article in articles:
            article.topics.add(topic)
        return user, {"search": content}, [article.id for article in articles]

    elif search_type == "non_existent":
        articles = ArticleFactory.create_batch(3, author=user)
        for article in articles:
            article.topics.add(topic)
        return user, {"search": "non_existent_term"}, []

@pytest.mark.django_db
@pytest.mark.parametrize(
    'search_data_factory',
    [
        "by_topic",
        "by_title",
        "by_summary",
        "by_content",
        "non_existent"
    ],
    indirect=True
)
def test_search_articles(search_data_factory, api_client, tokens):
    """
    The function tests the search functionality of articles.
    """
    user, query_params, expected_article_ids = search_data_factory
    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.get('/api/articles/', data=query_params)

    assert response.status_code == status.HTTP_200_OK

    if query_params.get("search") == "non_existent_term":
        assert len(response.data['results']) == 0
    else:
        returned_article_ids = [article['id'] for article in response.data['results']]
        assert set(expected_article_ids) == set(returned_article_ids), "Returned articles do not match the expected articles"
