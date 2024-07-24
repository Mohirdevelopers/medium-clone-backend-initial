import importlib.util
import pytest


def test_via_importlib():
    loader = importlib.util.find_spec('loguru')
    assert loader is not None, "loguru is not installed"


@pytest.mark.order(1)
@pytest.mark.django_db
def test_custom_logging_exists():
    try:
        from core.custom_logging import InterceptHandler  # noqa
    except ImportError:
        assert False, "custom_logging folder missing"


@pytest.mark.order(1)
@pytest.mark.django_db
def test_custom_middleware_exists():
    try:
        from core.middlewares import CustomLocaleMiddleware  # noqa
    except ImportError:
        assert False, "CustomLocaleMiddleware not created"
