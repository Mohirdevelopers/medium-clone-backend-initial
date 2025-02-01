import pytest
from django.contrib.auth import get_user_model
from faker import Faker

fake = Faker()

User = get_user_model()


@pytest.fixture()
@pytest.mark.order(1)
def article_delete_data(request, user_factory):
    """
    Fixture to provide data for DELETE article tests.
    """

    from tests.factories.article_factory import ArticleFactory

    user = user_factory.create()
    another_user = user_factory.create()
    article = ArticleFactory.create(author=user)

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
@pytest.mark.order(2)
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
        response = client.delete(f'/api/articles/{article_id}/')

        assert response.status_code == status_code

        from articles.models import Article

        if status_code == 204:
            article = Article.objects.filter(id=article_id).first()
            assert article.status == "trash", "Article is not deleted or not moved to trash"

            response = client.get(f'/api/articles/{article_id}/')
            assert response.status_code == 404

    except Exception:
        assert status_code == 403
