import pytest
import importlib.util
from django.conf import settings


@pytest.mark.order(1)
@pytest.mark.django_db
def test_django_resized():
    assert settings.DJANGORESIZED_DEFAULT_SIZE == [1920, 1080], "DJANGORESIZED_DEFAULT_SIZE is not set correctly"
    assert settings.DJANGORESIZED_DEFAULT_QUALITY == 80, "DJANGORESIZED_DEFAULT_QUALITY is not set correctly"
    assert settings.DJANGORESIZED_DEFAULT_SCALE == 1, "DJANGORESIZED_DEFAULT_SCALE is not set correctly"
    assert settings.DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS == {
        "JPEG": ".jpg"}, "DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS is not set correctly"
    assert settings.DJANGORESIZED_DEFAULT_KEEP_META, "DJANGORESIZED_DEFAULT_KEEP_META is not set correctly"
    assert settings.DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION, "DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION is not set correctly"

    loader = importlib.util.find_spec('django_resized')
    assert loader is not None, "django_resized is not installed"
