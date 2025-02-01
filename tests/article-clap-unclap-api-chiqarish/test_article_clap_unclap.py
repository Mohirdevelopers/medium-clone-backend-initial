import pytest
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.order(1)
def test_clap_view_exists():
    """
    Test if clap view exists.
    """

    from articles.views import ClapView

    assert ClapView, "ClapView not created"


@pytest.mark.order(2)
def test_clap_serializer_created():
    """
    The function tests that the clap serializer is created.
    """
    from articles.serializers import ClapSerializer

    assert ClapSerializer, "ClapSerializer not created"


@pytest.fixture()
@pytest.mark.order(3)
def clap_data(request, user_factory):
    """
    Fixture to provide data for clapping tests.
    """

    from tests.factories.article_factory import ArticleFactory
    from tests.factories.clap_factory import ClapFactory

    user = user_factory.create()
    article = ArticleFactory.create()

    def valid_clap():
        return (
            201, article.id, user, False
        )

    def already_clapped_max_count():
        ClapFactory.create(article=article, user=user, count=50)
        return (
            201, article.id, user, True
        )

    data = {
        "valid_clap": valid_clap,
        "already_clapped_max_count": already_clapped_max_count
    }

    return data[request.param]()


@pytest.mark.django_db
@pytest.mark.order(4)
@pytest.mark.parametrize(
    'clap_data',
    [
        "valid_clap",
        "already_clapped_max_count"
    ],
    indirect=True
)
def test_clap_article(clap_data, api_client, tokens):
    """
    Test clapping an article.
    """
    status_code, article_id, user, is_clapped = clap_data

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.post(f'/api/articles/{article_id}/clap/')

    assert response.status_code == status_code
    if is_clapped is not True:
        assert response.status_code == status_code
        assert response.data['count'] == 1
    if is_clapped:
        assert response.status_code == status_code
        assert response.data['count'] == 50


@pytest.fixture()
@pytest.mark.order(5)
def undo_clap_data(request, user_factory):
    """
    Fixture to provide data for undoing claps tests.
    """

    from tests.factories.article_factory import ArticleFactory
    from tests.factories.clap_factory import ClapFactory

    user = user_factory.create()
    article = ArticleFactory.create()
    no_clapped_article = ArticleFactory.create()

    ClapFactory.create(article=article, user=user)

    def valid_undo():
        return (
            204, article.id, user
        )

    def no_clap_to_undo():
        return (
            404, no_clapped_article.id, user
        )

    data = {
        "valid_undo": valid_undo,
        "no_clap_to_undo": no_clap_to_undo
    }

    return data[request.param]()


@pytest.mark.django_db
@pytest.mark.order(6)
@pytest.mark.parametrize(
    'undo_clap_data',
    [
        "valid_undo",
        "no_clap_to_undo"
    ],
    indirect=True
)
def test_undo_clap_article(undo_clap_data, api_client, tokens):
    """
    Test undoing a clap from an article.
    """
    status_code, article_id, user = undo_clap_data

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.delete(f'/api/articles/{article_id}/clap/')

    assert response.status_code == status_code

    if status_code == status.HTTP_404_NOT_FOUND:
        assert 'Not found.' in response.data['detail']
