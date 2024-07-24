import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status


@pytest.mark.order(1)
@pytest.mark.django_db
def test_swagger_schema(api_client):
    assert 'drf_spectacular' in settings.INSTALLED_APPS, "drf_spectacular package is not installed"
    assert 'DEFAULT_SCHEMA_CLASS' in settings.REST_FRAMEWORK, "DEFAULT_SCHEMA_CLASS package is not installed"
    assert hasattr(settings, 'SPECTACULAR_SETTINGS'), "SPECTACULAR_SETTINGS not found in settings"

    schema_path = reverse('schema')
    swagger_path = reverse('swagger-ui')
    redoc_path = reverse('redoc')

    assert schema_path == '/schema/', "Schema path is not configured correctly"
    assert swagger_path == '/swagger/', "Swagger path is not configured correctly"
    assert redoc_path == '/redoc/', "Redoc path is not configured correctly"

    response = api_client().get(swagger_path)
    assert response.status_code == status.HTTP_200_OK, f"Failed to fetch Swagger UI, received status code {response.status_code}"
    assert 'text/html' in response['Content-Type'], f"Expected HTML content, received {response['Content-Type']}"

    response = api_client().get(redoc_path)
    assert response.status_code == status.HTTP_200_OK, f"Failed to fetch Redoc, received status code {response.status_code}"
    assert 'text/html' in response['Content-Type'], f"Expected HTML content, received {response['Content-Type']}"

    response = api_client().get(schema_path)
    assert response.status_code == status.HTTP_200_OK, f"Failed to fetch Schema, received status code {response.status_code}"
    assert 'application/vnd.oai.openapi' in response[
        'Content-Type'], f"Expected vnd.oai.openapi content, received {response['Content-Type']}"
