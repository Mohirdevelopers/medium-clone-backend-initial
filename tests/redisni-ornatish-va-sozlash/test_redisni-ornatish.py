import pytest
from django.conf import settings
import importlib.util


@pytest.mark.order(1)
@pytest.mark.django_db
def test_redis_installed():
    loader = importlib.util.find_spec('redis')
    assert loader is not None, "django_redis package is not installed"

    assert 'django_redis' in settings.INSTALLED_APPS, "django_redis package is not installed"
    assert hasattr(settings, 'REDIS_HOST'), "REDIS_HOST not found in settings"
    assert hasattr(settings, 'REDIS_PORT'), "REDIS_PORT not found in settings"
    assert 'default' in settings.CACHES
    assert settings.CACHES['default']['BACKEND'] == 'django_redis.cache.RedisCache'
