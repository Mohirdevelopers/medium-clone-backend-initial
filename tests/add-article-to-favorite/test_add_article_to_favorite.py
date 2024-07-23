import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()

@pytest.fixture
def favorite_article_data(request, user_factory, article_factory):
    """
    Provides test data for adding articles to favorites.
    """
    user = user_factory.create()
    article = article_factory.create(author=user)
    added_article = article_factory.create(author=user)

    user.favorites.create(article=added_article)

    def add_favorite():
        return (
            201, article.id, user
        )

    def add_article_again_favorite():
        return (
            400, added_article.id, user
        )

    data = {
        "add_favorite": add_favorite,
        "add_article_again_favorite": add_article_again_favorite,
    }

    return data[request.param]()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "favorite_article_data",
    [
        "add_favorite",
        "add_article_again_favorite",
    ],
    indirect=True
)
def test_add_article_to_favorites(api_client, tokens, favorite_article_data):
    """
    Tests adding an article to the user's favorites.
    """
    status_code, article_id, user = favorite_article_data

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.post(f'/articles/{article_id}/favorite/')

    assert response.status_code == status_code

    if status_code == status.HTTP_201_CREATED:
        assert response.data['detail'] == "Maqola sevimlilarga qo'shildi."
    elif status_code == status.HTTP_400_BAD_REQUEST:
        assert response.data['detail'] == "Maqola sevimlilarga allaqachon qo'shilgan."



@pytest.fixture
def remove_favorite_article_data(request, user_factory, article_factory, favorite_factory):
    """
    Provides test data for removing articles from favorites.
    """
    user = user_factory.create()
    article = article_factory.create(author=user)

    favorite_factory.create(user=user, article=article)

    def remove_favorite():
        return (
            204, article.id, user
        )

    data = {
        "remove_favorite": remove_favorite
    }

    return data[request.param]()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "remove_favorite_article_data",
    [
        "remove_favorite"
    ],
    indirect=True
)
def test_remove_article_from_favorites(api_client, tokens, remove_favorite_article_data):
    """
    Tests removing an article from the user's favorites.
    """
    status_code, article_id, user = remove_favorite_article_data

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.delete(f'/articles/{article_id}/favorite/')

    assert response.status_code == status_code


@pytest.fixture
def retrieve_user_favorites_data(request, user_factory, article_factory, favorite_factory):
    """
    Provides test data for retrieving the user's favorite articles.
    """
    user = user_factory.create()
    articles = [
        article_factory.create(author=user),
        article_factory.create(author=user)
    ]

    # Assuming you have a Favorite model or similar for managing user favorites
    for article in articles:
        favorite_factory.create(user=user, article=article)

    def get_favorites():
        return (
            200, [article.id for article in articles], user
        )

    data = {
        "get_favorites": get_favorites
    }

    return data[request.param]()

@pytest.mark.django_db
@pytest.mark.parametrize(
    "retrieve_user_favorites_data",
    [
        "get_favorites"
    ],
    indirect=True
)
def test_retrieve_user_favorites(api_client, tokens, retrieve_user_favorites_data):
    """
    Tests retrieving the list of favorites for a user.
    """
    status_code, expected_article_ids, user = retrieve_user_favorites_data

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.get('/users/favorites/')

    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        favorite_articles = response.data.get('results', [])
        favorite_article_ids = [article['article']['id'] for article in favorite_articles]

        assert set(favorite_article_ids) == set(expected_article_ids)
