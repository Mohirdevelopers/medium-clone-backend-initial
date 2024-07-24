import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


@pytest.fixture
def change_password_data(request, user_factory, tokens):
    old_password = 'strong_password_123'
    new_password = 'new_password_123'
    user = user_factory.create(password=old_password)
    access, _ = tokens(user)

    def valid_password():
        return (
            200, user, access,
            {
                'old_password': old_password,
                'new_password': new_password
            }
        )

    def incorrect_password():
        return (
            400, user, access,
            {
                'old_password': '<PASSWORD>',
                'new_password': new_password
            }
        )

    def invalid_old_password():
        return (
            400, user, access,
            {
                'old_password': 'asdf*&^%',
                'new_password': new_password
            },
        )

    def empty_old_password():
        return (
            400, user, access,
            {
                'old_password': '',
                'new_password': new_password
            },
        )

    def required_old_password():
        return (
            400, user, access,
            {
                'new_password': new_password
            },
        )

    def invalid_new_password():
        return (
            400, user, access,
            {
                'old_password': old_password,
                'new_password': old_password
            },
        )

    def empty_new_password():
        return (
            400, user, access,
            {
                'old_password': old_password,
                'new_password': ''
            },
        )

    def required_new_password():
        return (
            400, user, access,
            {
                'old_password': old_password,
            },
        )

    def inactive_user():
        user.is_active = False
        user.save()
        return 401, user, 'fake-token', {}

    def unauthorized_user():
        return 401, user, 'fake-token', {}

    data = {
        'valid_password': valid_password,
        'incorrect_password': incorrect_password,
        'invalid_old_password': invalid_old_password,
        'empty_old_password': empty_old_password,
        'required_old_password': required_old_password,
        'invalid_new_password': invalid_new_password,
        'empty_new_password': empty_new_password,
        'required_new_password': required_new_password,
        'inactive_user': inactive_user,
        'unauthorized_user': unauthorized_user
    }
    return data[request.param]


@pytest.mark.django_db
@pytest.mark.parametrize(
    'change_password_data',
    [
        'valid_password',
        'incorrect_password',
        'invalid_old_password',
        'empty_old_password',
        'required_old_password',
        'invalid_new_password',
        'empty_new_password',
        'required_new_password',
        'inactive_user',
        'unauthorized_user'
    ],
    indirect=True,
)
def test_change_password(change_password_data, api_client):
    status_code, user, access, data = change_password_data()
    client = api_client(token=access)
    resp = client.put('/users/password/change/', data, format='json')
    assert resp.status_code == status_code

    if resp.status_code == status.HTTP_200_OK:
        user.refresh_from_db()
        assert user.check_password(data['new_password'])

        client = api_client()
        login_url = '/users/login/'
        login_data = {
            'username': user.username,
            'password': data['new_password']
        }

        login_resp = client.post(login_url, login_data, format='json')

        resp_json = login_resp.json()
        assert sorted(resp_json.keys()) == sorted(['access', 'refresh'])
