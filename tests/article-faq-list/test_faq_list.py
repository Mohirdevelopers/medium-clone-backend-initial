import pytest
from rest_framework import status


@pytest.mark.django_db
def test_faq_list_view(api_client, faq_factory):
    """
    Test the FAQListView for retrieving a list of FAQs.
    """

    faq_factory.create()
    faq_factory.create()

    client = api_client()
    response = client.get('/articles/faqs/')

    assert response.status_code == status.HTTP_200_OK

    assert len(response.data['results']) == 2
