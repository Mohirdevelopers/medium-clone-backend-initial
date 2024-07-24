import pytest
from django.conf import settings
import importlib.util


@pytest.mark.order(1)
@pytest.mark.django_db
def test_ckeditor_installed():
    loader = importlib.util.find_spec('ckeditor')
    assert loader is not None, "ckeditor package is not installed"

    assert 'ckeditor' in settings.INSTALLED_APPS, "ckeditor package is not installed"
    assert hasattr(settings, 'CKEDITOR_CONFIGS'), "CKEDITOR_CONFIGS not found in settings"
    assert hasattr(settings, 'CKEDITOR_BASEPATH'), "CKEDITOR_BASEPATH not found in settings"
