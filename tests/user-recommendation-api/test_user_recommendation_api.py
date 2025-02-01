import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from faker import Faker

fake = Faker()

User = get_user_model()


@pytest.mark.order(1)
def test_recommendation_model_created():
    """
    The function tests the creation of the RecommendationView model.
    """

    from users.models import Recommendation
    assert Recommendation, "Recommendation model not created"
    assert Recommendation._meta.db_table == "recommendation", "Recommendation model not created"
    assert Recommendation._meta.verbose_name == "Recommendation", "Recommendation model not created"
    assert Recommendation._meta.verbose_name_plural == "Recommendations", "Recommendation model not created"
    assert Recommendation._meta.ordering == ["-created_at"], "Recommendation model not created"


@pytest.mark.order(2)
def test_recommendation_serializer_created():
    """
    The function tests the creation of the RecommendationSerializer model.
    """

    from users.serializers import RecommendationSerializer
    assert RecommendationSerializer, "RecommendationSerializer not created"


@pytest.mark.order(3)
def test_recommendation_view_created():
    """
    The function tests the creation of the RecommendationView model.
    """

    from users.views import RecommendationView
    assert RecommendationView, "RecommendationView not created"


@pytest.fixture
@pytest.mark.order(4)
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
@pytest.mark.order(5)
def test_articles(articles_data, api_client, tokens):
    """
    The function tests the articles.
    """

    articles, _, user = articles_data
    access, _ = tokens(user)

    response = api_client(token=access).get('/api/articles/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 5


@pytest.mark.django_db
@pytest.mark.order(6)
def test_articles_more_recommendations(articles_data, api_client, tokens):
    """
    The function tests the association between articles and more recommendations.
    """

    articles, topics, user = articles_data
    access, _ = tokens(user)
    client = api_client(token=access)

    topic_id = articles[0].topics.first().id
    article_id = articles[0].id

    data = {
        "less_article_id": article_id
    }

    response = client.post('/api/users/recommend/', data=data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    data = {
        "more_article_id": article_id
    }

    response = client.post('/api/users/recommend/', data=data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get('/api/articles/?is_recommend=true')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'][0]['topics'][0]['id'] == topic_id


@pytest.mark.django_db
@pytest.mark.order(7)
def test_articles_less_recommendations(articles_data, api_client, tokens):
    """
    The function tests the association between articles and less recommendations.
    """

    articles, topics, user = articles_data
    access, _ = tokens(user)
    client = api_client(token=access)

    articles[0].topics.first().id
    article_id = articles[0].id

    data = {
        "more_article_id": article_id
    }

    more_response = client.post('/api/users/recommend/', data=data, format='json')
    assert more_response.status_code == status.HTTP_204_NO_CONTENT

    data = {
        "less_article_id": article_id
    }

    response = client.post('/api/users/recommend/', data=data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get('/api/articles/?is_recommend=true')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 0
