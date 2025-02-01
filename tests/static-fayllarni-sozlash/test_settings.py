import pytest
from django.conf import settings
from django.conf.urls.static import static
from core.urls import urlpatterns


def test_constants_exists():
    assert settings.STATIC_URL == '/static/', "STATIC_URL is not set correctly"
    assert settings.STATIC_ROOT == settings.BASE_DIR / "static", "STATIC_ROOT is not set correctly"


static_url = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = urlpatterns
