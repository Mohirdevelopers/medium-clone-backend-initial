import pytest
from django.conf import settings
import importlib.util


@pytest.mark.order(1)
def test_env_example_file():
    required_settings = [
        "REDIS_HOST",
        "REDIS_PORT",
        "REDIS_DB"
    ]

    try:
        with open(".env.example", "r") as file:
            content = file.read()
            for setting in required_settings:
                assert f"{setting}=" in content, f"{setting} is missing in .env.example"
    except FileNotFoundError:
        pytest.fail(".env.example file is missing")


@pytest.mark.order(2)
def test_redis_installed():
    loader = importlib.util.find_spec('django_redis')
    assert loader is not None, "django-redis package is not installed"


@pytest.mark.order(3)
def test_redis_configured():
    assert 'django_redis' in settings.INSTALLED_APPS, "django-redis package is not added to settings"
    assert hasattr(settings, 'REDIS_HOST'), "REDIS_HOST not found in settings"
    assert hasattr(settings, 'REDIS_PORT'), "REDIS_PORT not found in settings"
    assert 'default' in settings.CACHES
    assert settings.CACHES['default']['BACKEND'] == 'django_redis.cache.RedisCache'


@pytest.mark.order(4)
def test_redis_connection():
    from django_redis import get_redis_connection
    c = get_redis_connection('default')
    c.set('test_key', 'test_value')
    cached_value = c.get('test_key')
    assert cached_value == b'test_value', "redis is not working"
