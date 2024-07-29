import pytest
import fakeredis
from pytest_factoryboy import register
from tests.factories.user_factory import UserFactory

try:
    from rest_framework.test import APIClient
except ImportError:
    pass

try:
    from rest_framework_simplejwt.tokens import RefreshToken
except ImportError:
    pass

register(UserFactory)


@pytest.fixture
def api_client():
    def _api_client(token=None):
        client = APIClient(raise_request_exception=False)
        if token:
            client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        return client

    return _api_client


@pytest.fixture
def tokens():
    def _tokens(user):
        refresh = RefreshToken.for_user(user)
        access = str(getattr(refresh, 'access_token'))
        return access, refresh

    return _tokens


@pytest.fixture
def fake_redis():
    return fakeredis.FakeRedis()
