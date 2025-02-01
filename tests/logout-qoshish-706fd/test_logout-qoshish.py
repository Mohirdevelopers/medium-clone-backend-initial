import pytest
from django.contrib.auth import get_user_model
from enum import Enum

User = get_user_model()


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


@pytest.fixture
def logout_data(request, user_factory, api_client, tokens, mocker):
    def valid_without_stored_tokens():
        user = user_factory.create()
        access, _ = tokens(user)
        return 200, api_client(access), user, access

    def valid_with_stored_tokens():
        user = user_factory.create()
        access, _ = tokens(user)
        return 200, api_client(access), user, access

    def invalid_with_unauthorized_user():
        return 401, api_client(), mocker.Mock(id="f0f9f100-3abd-4bbf-88ad-0cfdd6953aca"), None

    data = {
        'valid_without_stored_tokens': valid_without_stored_tokens,
        'valid_with_stored_tokens': valid_with_stored_tokens,
        'invalid_with_unauthorized_user': invalid_with_unauthorized_user,
    }
    return data[request.param]


@pytest.mark.django_db
@pytest.mark.parametrize(
    'logout_data',
    [
        'valid_without_stored_tokens',
        'valid_with_stored_tokens',
        'invalid_with_unauthorized_user',
    ],
    indirect=True,
)
def test_logout(logout_data, mocker, fake_redis, request, tokens):
    status_code, client, user, access = logout_data()
    test_name = request.node.name

    mocker.patch('users.services.TokenService.get_redis_client', return_value=fake_redis)

    # add tokens to fake_redis
    if test_name == 'test_logout[valid_with_stored_tokens]':
        _, refresh = tokens(user)
        access_token_key = f"user:{user.id}:{TokenType.ACCESS}"
        refresh_token_key = f"user:{user.id}:{TokenType.REFRESH}"
        fake_redis.sadd(access_token_key, access)
        fake_redis.sadd(refresh_token_key, str(refresh))

    # users-me get data
    if test_name == 'test_logout[valid_with_stored_tokens]':
        url = '/api/users/me/'
        resp = client.get(url)
        assert resp.status_code == status_code

    # logout
    resp = client.post('/api/users/logout/')
    assert resp.status_code == status_code
    # users-me get data after logout
    if status_code == 200:
        resp = client.get('/api/users/me/')
        assert resp.status_code == 401
