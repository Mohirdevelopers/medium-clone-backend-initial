from secrets import token_urlsafe
from unittest import mock
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import APIException

User = get_user_model()


class OTPException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'OTP verification failed.'
    default_code = 'otp_failed'


@pytest.fixture
def forgot_password_data(request, user_factory):
    user = user_factory.create()
    user.save()

    def valid_data():
        return (
            200, user,
            {
                'email': user.email,
            }
        )

    def not_exist_email():
        return (
            400, user,
            {
                'email': 'test@gmail.com',
            }
        )

    def invalid_email():
        return (
            400, user,
            {
                'email': 'testgmail.com',
            }
        )

    def empty_email():
        return (
            400, user,
            {
                'email': '',
            }
        )

    def required_email():
        return (
            400, user,
            {}
        )

    data = {
        'valid_data': valid_data,
        'not_exist_email': not_exist_email,
        'invalid_email': invalid_email,
        'empty_email': empty_email,
        'required_email': required_email,
    }
    return data[request.param]


@pytest.mark.django_db
@pytest.mark.parametrize(
    'forgot_password_data',
    [
        'valid_data',
        'not_exist_email',
        'invalid_email',
        'empty_email',
        'required_email'
    ],
    indirect=True,
)
def test_forgot_password_view(forgot_password_data, api_client, mocker):
    status_code, user, data = forgot_password_data()
    generate_otp_mock = mock.Mock(return_value=("567483", "sdNdFhKSt_0p2cbzygxcI9A75doUwSYocr1vTqkjxeM"))
    mocker.patch('users.services.OTPService.generate_otp', generate_otp_mock)
    mock_redis_conn = mocker.Mock()
    mocker.patch('users.services.OTPService.get_redis_conn', return_value=mock_redis_conn)
    client = api_client()
    resp = client.post('/api/users/password/forgot/', data, format='json')
    assert resp.status_code == status_code
    if status_code == status.HTTP_200_OK:
        resp_json = resp.json()
        assert sorted(resp_json.keys()) == sorted(['email', 'otp_secret'])
        assert resp.data['email'] == user.email

        # check send email error
        key = f"{user.email}:otp"
        mocker.patch(
            'users.services.SendEmailService.send_email',
            mock.Mock(side_effect=Exception('Error sending email.'))
        )
        resp = client.post('/api/users/password/forgot/', data, format='json')
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        mock_redis_conn.delete.assert_called_once_with(key)


@pytest.fixture
def forgot_password_verify_data(request, user_factory, mocker):
    user = user_factory.create()

    otp_code = "123456"
    otp_secret = "sdNdFhKSt_0p2cbzygxcI9A75doUwSYocr1vTqkjxeM"

    def valid_data():
        return (
            200, user, otp_secret, None,
            {
                'email': user.email,
                'otp_code': otp_code,
            }
        )

    def not_exist_email():
        return (
            404, user, otp_secret, None,
            {
                'email': 'test@gmail.com',
                'otp_code': otp_code,
            }
        )

    def inactive_user():
        user.is_active = False
        user.save()
        return (
            404, user, otp_secret, None,
            {
                'email': user.email,
                'otp_code': otp_code,
            }
        )

    def invalid_email():
        return (
            400, user, otp_secret, None,
            {
                'email': 'fake_email',
                'otp_code': otp_code,
            }
        )

    def empty_email():
        return (
            400, user, otp_secret, None,
            {
                'email': '',
                'otp_code': otp_code,
            }
        )

    def required_email():
        return (
            400, user, otp_secret, None,
            {
                'otp_code': otp_code,
            }
        )

    def invalid_otp_code():
        return (
            400, user, otp_secret, OTPException('Invalid OTP code.'),
            {
                'email': user.email,
                'otp_code': '000000',
            }
        )

    def empty_otp_code():
        return (
            400, user, otp_secret, None,
            {
                'email': user.email,
                'otp_code': '',
            }
        )

    def required_otp_code():
        return (
            400, user, otp_secret, None,
            {
                'email': user.email,
            }
        )

    def invalid_otp_secret():
        return (
            400, user, 'fake-otp-secret', OTPException('Invalid OTP code.'),
            {
                'email': user.email,
                'otp_code': otp_code,
            }
        )

    def empty_otp_secret():
        return (
            404, user, '', None,
            {
                'email': user.email,
                'otp_code': otp_code,
            }
        )

    def required_otp_secret():
        return (
            404, user, '', None,
            {
                'email': user.email,
                'otp_code': otp_code,
            }
        )

    data = {
        'valid_data': valid_data,
        'not_exist_email': not_exist_email,
        'inactive_user': inactive_user,
        'invalid_email': invalid_email,
        'empty_email': empty_email,
        'required_email': required_email,
        'invalid_otp_code': invalid_otp_code,
        'empty_otp_code': empty_otp_code,
        'required_otp_code': required_otp_code,
        'invalid_otp_secret': invalid_otp_secret,
        'empty_otp_secret': empty_otp_secret,
        'required_otp_secret': required_otp_secret,
    }
    return data[request.param]


@pytest.mark.django_db
@pytest.mark.parametrize(
    'forgot_password_verify_data',
    [
        'valid_data',
        'not_exist_email',
        'inactive_user',
        'invalid_email',
        'empty_email',
        'required_email',
        'invalid_otp_code',
        'empty_otp_code',
        'required_otp_code',
        'invalid_otp_secret',
        'empty_otp_secret',
        'required_otp_secret',
    ],
    indirect=True,
)
def test_forgot_password_verify_view(forgot_password_verify_data, api_client, mocker):
    status_code, user, otp_secret, check_otp_side_effect, data = forgot_password_verify_data()
    redis_conn = mocker.Mock()
    mocker.patch('users.services.OTPService.get_redis_conn', return_value=redis_conn)
    mocker.patch('users.services.OTPService.check_otp', side_effect=check_otp_side_effect)
    mock_token_hash = make_password(token_urlsafe())
    mocker.patch('users.views.make_password', return_value=mock_token_hash)
    client = api_client()
    resp = client.post(f'/api/users/password/forgot/verify/{otp_secret}/', data, format='json')
    assert resp.status_code == status_code
    if resp.status_code == status.HTTP_200_OK:
        resp_json = resp.json()
        key = f"{user.email}:otp"
        redis_conn.delete.assert_called_once_with(key)
        redis_conn.set.assert_called_once_with(mock_token_hash, user.email, ex=2 * 60 * 60)
        assert 'token' in resp_json
        assert resp_json['token'] == mock_token_hash


@pytest.fixture
def reset_password_view_data(request, user_factory):
    user = user_factory.create()
    token_hash = make_password(token_urlsafe())
    new_password = "new_password123"

    def valid_data():
        return (
            200, user.email, {
                "token": token_hash,
                "password": new_password
            }
        )

    def inactive_user():
        user.is_active = False
        user.save()
        return (
            404, user.email, {
                "token": token_hash,
                "password": new_password
            }
        )

    def not_exist_email():
        return (
            404, 'not_exist_email', {
                "token": token_hash,
                "password": new_password
            }
        )

    def empty_token():
        return (
            400, user.email, {
                "token": '',
                "password": new_password
            }
        )

    def required_token():
        return (
            400, user.email, {
                "password": new_password
            }
        )

    def invalid_password():
        return (
            400, user.email, {
                "token": token_hash,
                "password": '123'
            }
        )

    def empty_password():
        return (
            400, user.email, {
                "token": token_hash,
                "password": ''
            }
        )

    def required_password():
        return (
            400, user.email, {
                "token": token_hash
            }
        )

    data = {
        'valid_data': valid_data,
        'inactive_user': inactive_user,
        'not_exist_email': not_exist_email,
        'empty_token': empty_token,
        'required_token': required_token,
        'invalid_password': invalid_password,
        'empty_password': empty_password,
        'required_password': required_password
    }
    return data[request.param]


@pytest.mark.django_db
@pytest.mark.parametrize(
    'reset_password_view_data',
    [
        'valid_data',
        'inactive_user',
        'not_exist_email',
        'empty_token',
        'required_token',
        'invalid_password',
        'empty_password',
        'required_password',

    ],
    indirect=True,
)
def test_reset_password_view(reset_password_view_data, api_client, mocker):
    status_code, email, data = reset_password_view_data()
    mock_redis_conn = mocker.Mock()
    mocker.patch('users.services.OTPService.get_redis_conn', return_value=mock_redis_conn)
    mocker.patch('users.services.UserService.create_tokens',
                 return_value={'access': 'access_token', 'refresh': 'refresh_token'})
    mock_redis_conn.get.return_value = email.encode() if email else None

    client = api_client()
    resp = client.patch('/api/users/password/reset/', data, format='json')

    if resp.status_code != 400:
        mock_redis_conn.get.assert_called_once_with(data['token'])

    assert resp.status_code == status_code
    if resp.status_code == status.HTTP_200_OK:
        mock_redis_conn.delete.assert_called_once_with(data['token'])
        resp_json = resp.json()
        assert sorted(resp_json.keys()) == sorted(['access', 'refresh'])

        user = User.objects.get(email=email)
        assert user.check_password(data['password']) is True
