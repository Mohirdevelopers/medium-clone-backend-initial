import pytest
import fakeredis
from pytest_factoryboy import register
try:
    from rest_framework.test import APIClient
except ImportError:
    pass

try:
    from rest_framework_simplejwt.tokens import RefreshToken
except ImportError:
    pass
try:
    from tests.factories.article_factory import (
        ArticleFactory, TopicFactory, CommentFactory,
        FavoriteFactory, ClapFactory, ReadingHistoryFactory,
        FollowFactory, PinFactory, NotificationFactory, FAQFactory)
except Exception:
    pass
from tests.factories.user_factory import UserFactory

try:
    register(UserFactory)
    register(ArticleFactory)
    register(TopicFactory)
    register(CommentFactory)
    register(FavoriteFactory)
    register(ClapFactory)
    register(ReadingHistoryFactory)
    register(FollowFactory)
    register(PinFactory)
    register(NotificationFactory)
    register(FAQFactory)
except Exception:
    pass


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
