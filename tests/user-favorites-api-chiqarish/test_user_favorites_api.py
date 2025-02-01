import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.mark.order(1)
def test_favorite_model_created():
    """
    Tests that the Favorite model is created.
    """
    from articles.models import Favorite
    assert Favorite._meta.db_table == "favorite", "Favorite model not created"
    assert Favorite._meta.verbose_name == "Favorite", "Favorite model not created"
    assert Favorite._meta.verbose_name_plural == "Favorites", "Favorite model not created"
    assert Favorite._meta.ordering == ["-created_at"], "Favorite model not created"


@pytest.mark.order(2)
def test_favorite_article_view_created():
    """
    Tests that the FavoriteArticleView view is created.
    """
    from articles.views import FavoriteArticleView
    assert FavoriteArticleView, "FavoriteArticleView not created"


@pytest.fixture()
@pytest.mark.order(3)
def article_data(request, user_factory):
    """
    Provides test data for favorite article tests.
    """
    from tests.factories.article_factory import ArticleFactory
    from tests.factories.favorite_factory import FavoriteFactory

    user = user_factory.create()
    article = ArticleFactory.create(author=user)
    added_article = ArticleFactory.create(author=user)
    FavoriteFactory.create(user=user, article=added_article)

    def add_favorite():
        return 201, article.id, user

    def add_article_again_favorite():
        return 400, added_article.id, user

    def remove_favorite():
        return 204, added_article.id, user

    data = {
        "add_favorite": add_favorite,
        "add_article_again_favorite": add_article_again_favorite,
        "remove_favorite": remove_favorite,
    }

    return data[request.param]()


@pytest.mark.django_db
@pytest.mark.order(4)
@pytest.mark.parametrize(
    "article_data",
    [
        "add_favorite",
        "add_article_again_favorite",
        "remove_favorite",
    ],
    indirect=True
)
def test_favorite_article(api_client, tokens, article_data):
    """
    Tests adding and removing an article from the user's favorites.
    """
    status_code, article_id, user = article_data

    access, _ = tokens(user)
    client = api_client(token=access)

    if status_code == 201 or status_code == 400:
        response = client.post(f'/api/articles/{article_id}/favorite/')
        assert response.status_code == status_code

        if status_code == status.HTTP_201_CREATED:
            assert response.data['detail'] == "Maqola sevimlilarga qo'shildi."
        elif status_code == status.HTTP_400_BAD_REQUEST:
            assert response.data['detail'] == "Maqola sevimlilarga allaqachon qo'shilgan."
    elif status_code == 204:
        client.post(f'/api/articles/{article_id}/favorite/')
        response = client.delete(f'/api/articles/{article_id}/favorite/')
        assert response.status_code == status_code


@pytest.fixture()
@pytest.mark.order(5)
def retrieve_user_favorites_data(user_factory):
    """
    Provides test data for retrieving the user's favorite articles.
    """
    from tests.factories.article_factory import ArticleFactory
    from tests.factories.favorite_factory import FavoriteFactory

    user = user_factory.create()
    articles = [ArticleFactory.create(author=user) for _ in range(2)]

    for article in articles:
        FavoriteFactory.create(user=user, article=article)

    return 200, [article.id for article in articles], user


@pytest.mark.django_db
@pytest.mark.order(6)
def test_retrieve_user_favorites(api_client, tokens, retrieve_user_favorites_data):
    """
    Tests retrieving the list of favorites for a user.
    """
    status_code, expected_article_ids, user = retrieve_user_favorites_data

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.get('/api/articles/?is_user_favorites=true')

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        favorite_articles = response.data.get('results', [])
        favorite_article_ids = [article['id'] for article in favorite_articles]

        assert set(favorite_article_ids) == set(expected_article_ids)
