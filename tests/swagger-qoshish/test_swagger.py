import pytest
import importlib.util
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

@pytest.mark.order(1)
def test_via_importlib():
    loader = importlib.util.find_spec('drf_spectacular')
    assert loader is not None, "drf_spectacular is not installed"


@pytest.mark.order(2)
@pytest.mark.django_db
def test_swagger_urls_set_correctly():
    schema_path = reverse('schema')
    swagger_path = reverse('swagger-ui')
    redoc_path = reverse('redoc')


    assert schema_path == '/api/schema/', "Schema path is not configured correctly"
    assert swagger_path == '/api/swagger/', "Swagger path is not configured correctly"
    assert redoc_path == '/api/redoc/', "Redoc path is not configured correctly"



@pytest.mark.order(3)
@pytest.mark.django_db
def test_swagger_schema_protected(client, user_factory):
    username = 'test'
    password = 'random_password'
    user = user_factory.create(username=username)
    user.set_password(password)
    user.save()

    swagger_path = reverse('swagger-ui')

    response = client.get(swagger_path)
    assert response.status_code == status.HTTP_302_FOUND, "Swagger is not protected"


@pytest.mark.order(4)
@pytest.mark.django_db
def test_swagger_schema(client, user_factory):
    get_user_model()
    username = 'test'
    password = 'random_password'
    user = user_factory.create(username=username)
    user.set_password(password)
    user.save()

    schema_path = reverse('schema')
    swagger_path = reverse('swagger-ui')
    redoc_path = reverse('redoc')

    client.login(username=username, password=password)

    assert 'drf_spectacular' in settings.INSTALLED_APPS, "drf_spectacular package is not installed"
    assert 'DEFAULT_SCHEMA_CLASS' in settings.REST_FRAMEWORK, "DEFAULT_SCHEMA_CLASS package is not installed"
    assert hasattr(settings, 'SPECTACULAR_SETTINGS'), "SPECTACULAR_SETTINGS not found in settings"

    assert schema_path == '/api/schema/', "Schema path is not configured correctly"
    assert swagger_path == '/api/swagger/', "Swagger path is not configured correctly"
    assert redoc_path == '/api/redoc/', "Redoc path is not configured correctly"

    response = client.get(swagger_path)
    assert response.status_code == status.HTTP_200_OK, f"Failed to fetch Swagger UI, received status code {response.status_code}"
    assert 'text/html' in response['Content-Type'], f"Expected HTML content, received {response['Content-Type']}"

    response = client.get(redoc_path)
    assert response.status_code == status.HTTP_200_OK, f"Failed to fetch Redoc, received status code {response.status_code}"
    assert 'text/html' in response['Content-Type'], f"Expected HTML content, received {response['Content-Type']}"

    response = client.get(schema_path)
    assert response.status_code == status.HTTP_200_OK, f"Failed to fetch Schema, received status code {response.status_code}"
    assert 'application/vnd.oai.openapi' in response['Content-Type'], f"Expected vnd.oai.openapi content, received {response['Content-Type']}"
