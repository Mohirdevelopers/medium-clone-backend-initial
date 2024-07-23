import os
import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

User = get_user_model()


@pytest.fixture
def user_update_data(request, user_factory, tokens):
    user = user_factory.create()
    access, _ = tokens(user)

    def valid_update():
        return (
            200,
            access,
            {
                'first_name': 'Abdulaziz',
                'last_name': 'Komilov',
                'middle_name': 'Sobirovich',
                'email': 'abdulaziz@email.com',
            }
        )

    def invalid_update():
        return (
            400,
            access,
            {
                'first_name': 'Abdulaziz',
                'last_name': 'Komilov',
                'email': 'userEmail'
            }
        )

    def empty_data():
        return (
            200,
            access,
            {
                'first_name': '',
                'last_name': '',
                'middle_name': '',
                'email': ''
            }
        )

    def unauthorized_user():
        return (
            401,
            "token",
            {
                'first_name': 'Name',
                'last_name': 'LastName',
                'middle_name': 'MiddleName',
                'email': 'email@test.com'
            }
        )

    def valid_update_with_avatar():
        return (
            200,
            access,
            {
                'first_name': 'abdulaziz',
                'last_name': 'komilov',
                'middle_name': 'sobirovich',
                'email': 'test@uz.uz',
                'avatar': (
                    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
                    b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
                    b'\x02\x4c\x01\x00\x3b'
                )
            }
        )

    data = {
        'valid_update': valid_update,
        'invalid_update': invalid_update,
        'empty_data': empty_data,
        'unauthorized_user': unauthorized_user,
        'valid_update_with_avatar': valid_update_with_avatar,
    }
    return data[request.param]


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user_update_data',
    [
        'valid_update',
        'invalid_update',
        'empty_data',
        'unauthorized_user',
        'valid_update_with_avatar',
    ],
    indirect=True,
)
def test_user_me_patch(user_update_data, api_client):
    status_code, access, update_data = user_update_data()

    client = api_client(token=access)
    url = '/users/me/'

    if 'avatar' in update_data:
        avatar_data = update_data['avatar']
        avatar_file = SimpleUploadedFile(f"{update_data['first_name']}.gif", avatar_data, content_type="image/gif")
        update_data['avatar'] = avatar_file
        resp = client.patch(url, data=update_data, format='multipart')
    else:
        resp = client.patch(url, data=update_data)

    assert resp.status_code == status_code

    if status_code == status.HTTP_200_OK:
        resp_json = resp.json()
        assert resp_json['first_name'] == update_data.get('first_name', '')
        assert resp_json['last_name'] == update_data.get('last_name', '')
        assert resp_json['middle_name'] == update_data.get('middle_name', '')
        assert resp_json['email'] == update_data.get('email', '')

        user = User.objects.get(id=resp_json['id'])
        assert user.first_name == update_data.get('first_name')
        assert user.last_name == update_data.get('last_name')
        assert user.middle_name == update_data.get('middle_name', '')
        assert user.email == update_data.get('email')

        if 'avatar' in update_data:
            user.refresh_from_db()
            assert user.avatar is not None, "Avatar was not uploaded correctly"
            avatar_path = user.avatar.name
            assert avatar_path.startswith(f'users/avatars/{user.username}')
            assert avatar_path.endswith('.gif'), f"Expected avatar path to end with '.gif', got '{avatar_path}'"
            expected_avatar_filename = f"{user.username}.gif"
            assert os.path.basename(
                avatar_path) == expected_avatar_filename, f"Avatar filename mismatch: expected '{expected_avatar_filename}', got '{os.path.basename(avatar_path)}'"
