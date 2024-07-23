import importlib.util
import pytest
from django.conf import settings

def test_via_importlib():
    loader = importlib.util.find_spec('rest_framework')
    assert loader is not None, "djangorestframework is not installed"

@pytest.mark.order(1)
@pytest.mark.django_db
def test_swagger_schema(api_client):
    assert 'rest_framework' in settings.INSTALLED_APPS, "rest_framework package is not installed"
    assert 'DEFAULT_AUTHENTICATION_CLASSES' in settings.REST_FRAMEWORK, "DEFAULT_AUTHENTICATION_CLASSES not in REST_FRAMEWORK"
