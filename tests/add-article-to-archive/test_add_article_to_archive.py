import pytest
from rest_framework import status

@pytest.fixture
def article_data(article_factory, user_factory):
    """
    Fixture to provide data for article actions.
    """
    user = user_factory.create()
    article = article_factory.create(author=user)
    return article, user


@pytest.mark.django_db
def test_archive_article(api_client, tokens, article_data):
    """
    Test archiving an article.
    """
    article, user = article_data
    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.post(f'/articles/{article.id}/archive/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['detail'] == "Maqola arxivlandi."


@pytest.mark.django_db
def test_pin_article(api_client, tokens, article_data):
    """
    Test pinning an article.
    """
    article, user = article_data
    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.post(f'/articles/{article.id}/pin/')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['detail'] == "Maqola pin qilindi."

    user_response = client.get('/users/me/articles/')
    pinned_article_ids = [item['id'] for item in user_response.data['results']]
    assert len(pinned_article_ids) > 0
    assert pinned_article_ids[0] == article.id

    response = client.post(f'/articles/{article.id}/pin/')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_unpin_article(api_client, tokens, article_data):
    """
    Test unpinning an article.
    """
    article, user = article_data
    access, _ = tokens(user)
    client = api_client(token=access)

    client.post(f'/articles/{article.id}/pin/')

    response = client.delete(f'/articles/{article.id}/unpin/')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    response = client.delete(f'/articles/{article.id}/unpin/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == "Maqola topilmadi.."
