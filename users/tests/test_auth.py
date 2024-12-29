import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.fixture()
def login_user(api_client):
    sample = {
        "username": "mahdi",
        "password": "#$mSMm42Wf",
    }
    payload = {**sample, **{
        "first_name": "mahdi",
        "last_name": "ashtian"
    }}
    user = User.objects.create_user(**payload)

    def do_login_user(test_payload: dict = sample):
        data = {**sample, **test_payload}
        url = reverse('user:jwt-create')
        return api_client.post(url, data=data)

    return do_login_user


@pytest.fixture()
def logout_user(api_client):
    def do_logout_user():
        url = reverse('user:jwt-logout')
        return api_client.post(url)

    return do_logout_user


@pytest.mark.django_db
class TestLoginUser:
    def test_if_valid_data_returns_200(self, login_user):
        response = login_user()
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('access')
        assert response.data.get('refresh')

    def test_if_invalid_data_returns_400(self, login_user):
        data = {"username": "", "password": ""}
        response = login_user(data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not response.data.get('access')
        assert not response.data.get('refresh')


@pytest.mark.django_db
class TestLogoutUser:
    def test_if_user_is_authenticated_returns_200(self, logout_user, authenticate):
        authenticate()
        response = logout_user()
        assert response.status_code == status.HTTP_200_OK
        assert response.cookies.get('access', True)
        assert response.cookies.get('refresh', True)
