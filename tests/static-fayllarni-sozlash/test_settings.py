import pytest
from django.conf import settings


def test_constants_exists():
    assert settings.STATIC_URL == '/static/', "STATIC_URL is not set correctly"
    assert settings.STATIC_ROOT == settings.BASE_DIR / "static", "STATIC_ROOT is not set correctly"
