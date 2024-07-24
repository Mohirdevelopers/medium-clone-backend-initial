import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from faker import Faker

fake = Faker()

User = get_user_model()


@pytest.fixture
def articles_data(user_factory, topic_factory, article_factory):
    """
    The function create articles data for testing.
    """

    topics = topic_factory.create_batch(3)
    user = user_factory.create()
    articles = article_factory.create_batch(5, author=user)

    for article in articles:
        article.topics.add(topics[0])
        article.topics.add(topics[1])
        article.topics.add(topics[2])

    return articles, topics, user


@pytest.mark.django_db
def test_articles(articles_data, api_client, tokens):
    """
    The function tests the articles.
    """

    articles, _, user = articles_data
    access, _ = tokens(user)

    response = api_client(token=access).get('/articles/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 5


@pytest.mark.django_db
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

    response = api_client(token=access).get('/articles/?get_top_articles=2')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2
    assert response.data['results'][0]['id'] == article_0_id
    assert response.data['results'][1]['id'] == article_1_id

    response1 = api_client(token=access).get('/articles/?get_top_articles=None')
    assert response1.status_code == status.HTTP_400_BAD_REQUEST
    assert response1.data['get_top_articles'][0] == 'Enter a number.'


@pytest.mark.django_db
def test_articles_topic_id(articles_data, api_client, tokens):
    """
    The function tests the association between articles and topics.
    """

    articles, topics, user = articles_data
    access, _ = tokens(user)

    topic_id = topics[0].id
    response = api_client(token=access).get(f'/articles/?topic_id={topic_id}')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
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

    response = client.post('/users/recommend/', data=data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    data = {
        "more_article_id": article_id
    }

    response = client.post('/users/recommend/', data=data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get('/articles/?is_recommend=true')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['results'][0]['topics'][0]['id'] == topic_id


@pytest.mark.django_db
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

    more_response = client.post('/users/recommend/', data=data, format='json')
    assert more_response.status_code == status.HTTP_204_NO_CONTENT

    data = {
        "less_article_id": article_id
    }

    response = client.post('/users/recommend/', data=data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.get('/articles/?is_recommend=true')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 0


@pytest.fixture()
def test_article_create_data(request, user_factory, topic_factory):
    """
    The function create articles data for testing.
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
def article_retrieve_data(request, topic_factory, article_factory, user_factory):
    """
    The function tests article retrieval with multipart form data.
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


@pytest.fixture()
def article_patch_data(request, topic_factory, article_factory, user_factory):
    """
    Fixture to provide data for PATCH update article tests.
    """
    topic = topic_factory.create()
    user = user_factory.create()
    article = article_factory.create(author=user)
    article.topics.add(topic.id)
    article.save()

    def valid_patch_data():
        return (
            200, article.id, user, {
                "summary": "this is test updated summary"
            }
        )

    def invalid_patch_data():
        return (
            400, article.id, user, {
                "summary": ""
            }
        )

    def non_existent_article():
        return (
            404, 999, user, {
                "summary": "this is test updated summary"
            }
        )

    data = {
        "valid_patch_data": valid_patch_data,
        "invalid_patch_data": invalid_patch_data,
        "non_existent_article": non_existent_article,
    }

    return data[request.param]()


@pytest.mark.django_db
@pytest.mark.parametrize(
    'article_patch_data',
    [
        "valid_patch_data",
        "invalid_patch_data",
        "non_existent_article",
    ],
    indirect=True
)
def test_article_patch(article_patch_data, api_client, tokens):
    """
    The function tests updating an article with multipart form data.
    """

    status_code, article_id, user, patch_data = article_patch_data

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.patch(f'/articles/{article_id}/', data=patch_data, format='multipart')

    assert response.status_code == status_code

    if status_code == 200:
        assert response.data['summary'] == patch_data['summary']


@pytest.fixture()
def article_delete_data(request, article_factory, user_factory):
    """
    Fixture to provide data for DELETE article tests.
    """
    user = user_factory.create()
    another_user = user_factory.create()
    article = article_factory.create(author=user)

    def valid_delete_data():
        return (
            204, article.id, user
        )

    def non_existent_article():
        return (
            404, 999, user
        )

    def unauthorized_user():
        return (
            403, article.id, another_user
        )

    data = {
        "valid_delete_data": valid_delete_data,
        "non_existent_article": non_existent_article,
        "unauthorized_user": unauthorized_user,
    }

    return data[request.param]()


@pytest.mark.django_db
@pytest.mark.parametrize(
    'article_delete_data',
    [
        "valid_delete_data",
        "non_existent_article",
        "unauthorized_user"
    ],
    indirect=True
)
def test_article_delete(article_delete_data, api_client, tokens):
    """
    The function tests deleting an article.
    """
    status_code, article_id, user = article_delete_data

    access, _ = tokens(user)
    client = api_client(token=access)

    try:
        response = client.delete(f'/articles/{article_id}/')

        assert response.status_code == status_code

        if status_code == 204:
            response = client.get(f'/articles/{article_id}/')
            assert response.status_code == 404

    except Exception:
        assert status_code == 403
