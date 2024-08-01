import pytest
from rest_framework import status


@pytest.mark.order(1)
def test_report_model_exists():
    """
    Test that the Report model exists.
    """
    from articles.models import Report
    assert Report, "Report model not created"


@pytest.fixture
@pytest.mark.order(2)
def article_data(user_factory):
    """
    Fixture to create a sample article.
    """

    from tests.factories.article_factory import ArticleFactory

    user = user_factory.create()
    article = ArticleFactory.create()
    return user, article


@pytest.fixture
@pytest.mark.order(3)
def report_data(article_data):
    """
    Fixture to create a report.
    """
    user, article = article_data
    return user, article


@pytest.mark.django_db
@pytest.mark.order(4)
@pytest.mark.parametrize(
    'article_status, expected_status, expected_detail',
    [
        ("publish", status.HTTP_201_CREATED, "Shikoyat yuborildi."),
        ("trash", status.HTTP_404_NOT_FOUND, "No Article matches the given query."),
    ]
)
def test_report_article(api_client, tokens, report_data, article_status, expected_status, expected_detail):
    """
    Test reporting an article under different scenarios.
    """
    user, article = report_data
    article.status = article_status
    article.save()

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.post(f'/articles/{article.id}/report/')

    assert response.status_code == expected_status
    print("response data", response.data['detail'])
    if isinstance(response.data, dict):
        assert response.data.get('detail') == expected_detail
    elif isinstance(response.data, list):
        assert response.data[0] == expected_detail
    else:
        pytest.fail("Response data is not in expected format")

    if article_status == "publish":
        response = client.post(f'/articles/{article.id}/report/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        if isinstance(response.data, dict):
            assert response.data.get('detail') == "Ushbu maqola allaqachon shikoyat qilingan."
        elif isinstance(response.data, list):
            assert response.data[0] == "Ushbu maqola allaqachon shikoyat qilingan."
        else:
            pytest.fail("Response data is not in expected format")


@pytest.mark.django_db
@pytest.mark.order(5)
def test_report_article_twice(api_client, tokens, report_data):
    """
    Test attempting to report the same article twice by the same user.
    """
    user, article = report_data
    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.post(f'/articles/{article.id}/report/')
    assert response.status_code == status.HTTP_201_CREATED
    if isinstance(response.data, dict):
        assert response.data.get('detail') == "Shikoyat yuborildi."
    elif isinstance(response.data, list):
        assert response.data[0] == "Shikoyat yuborildi."
    else:
        pytest.fail("Response data is not in expected format")

    response = client.post(f'/articles/{article.id}/report/')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == "Ushbu maqola allaqachon shikoyat qilingan."


@pytest.mark.django_db
@pytest.mark.order(6)
def test_report_article_third(api_client, tokens, report_data, user_factory):
    """
    Test attempting to report the same article twice by the same user.
    """
    user, article = report_data
    access, _ = tokens(user)
    client = api_client(token=access)
    client.post(f'/articles/{article.id}/report/')

    user = user_factory.create()
    access, _ = tokens(user)
    client = api_client(token=access)
    client.post(f'/articles/{article.id}/report/')

    user = user_factory.create()
    access, _ = tokens(user)
    client = api_client(token=access)
    client.post(f'/articles/{article.id}/report/')

    user = user_factory.create()
    access, _ = tokens(user)
    client = api_client(token=access)
    response = client.post(f'/articles/{article.id}/report/')
    print("data response", response.data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['detail'] == "Maqola bir nechta shikoyatlar tufayli olib tashlandi."


@pytest.mark.django_db
@pytest.mark.order(7)
def test_report_unpublished_article(api_client, tokens, report_data):
    """
    Test reporting an unpublished article.
    """
    user, article = report_data
    article.status = "draft"
    article.save()

    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.post(f'/articles/{article.id}/report/')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert response.data['detail'] == "No Article matches the given query."


@pytest.mark.django_db
@pytest.mark.order(8)
def test_report_non_existing_article(api_client, tokens, user_factory):
    """
    Test reporting a non-existing article.
    """
    user = user_factory.create()
    access, _ = tokens(user)
    client = api_client(token=access)

    response = client.post('/articles/999999/report/')
    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert response.data.get('detail') == "No Article matches the given query."
