import pytest
from rest_framework import status


@pytest.mark.order(1)
def test_faq_model_exists():
    """
    Test that the FAQ model exists.
    """
    from articles.models import FAQ
    assert FAQ, "FAQ model not created"


@pytest.mark.django_db
@pytest.mark.order(2)
def test_faq_list_view(api_client):
    """
    Test the FAQListView for retrieving a list of FAQs.
    """

    from tests.factories.faq_factory import FAQFactory

    FAQFactory.create()
    FAQFactory.create()

    client = api_client()
    response = client.get('/api/articles/faqs/')

    assert response.status_code == status.HTTP_200_OK

    assert len(response.data['results']) == 2
