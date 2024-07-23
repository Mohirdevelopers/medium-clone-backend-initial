import pytest
from django.conf import settings


@pytest.mark.order(1)
@pytest.mark.django_db
def test_ckeditor_installed():
    try:
        import ckeditor  # noqa
    except ImportError:
        assert False, "ckeditor package is not installed"
    assert 'ckeditor' in settings.INSTALLED_APPS, "ckeditor package is not installed"
    assert hasattr(settings, 'CKEDITOR_CONFIGS'), "CKEDITOR_CONFIGS not found in settings"
    assert hasattr(settings, 'CKEDITOR_BASEPATH'), "CKEDITOR_BASEPATH not found in settings"
