import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

User = get_user_model()


@pytest.fixture()
def create_user(api_client):
    sample = {
        "username": "mahdiashtian",
        "password": "#$mSMm42Wf",
        "first_name": "mahdi",
        "last_name": "ashtian"
    }

    def do_create_user(test_payload: dict = sample):
        data = {**sample, **test_payload}
        url = reverse('user:user-list')
        return api_client.post(url, data=data)

    return do_create_user


@pytest.fixture()
def list_user(api_client):
    users = baker.make(User, _quantity=18)

    def do_list_user():
        url = reverse('user:user-list')
        return api_client.get(url)

    return do_list_user


@pytest.fixture()
def retrieve_user(api_client):
    user = baker.make(User)

    def do_retrieve_user(pk=user.id):
        url = reverse('user:user-detail', kwargs={'pk': pk})
        return api_client.get(url)

    return do_retrieve_user


@pytest.fixture()
def remove_user(api_client):
    user = baker.make(User)

    def do_remove_user(pk=user.id):
        url = reverse('user:user-detail', kwargs={'pk': pk})
        return api_client.delete(url)

    return do_remove_user


@pytest.mark.django_db
class TestCreateUser:
    def test_if_valid_data_returns_201(self, create_user):
        response = create_user()
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_invalid_data_returns_400(self, create_user):
        data = {"username": "", "password": "", "first_name": "", "last_name": ""}
        response = create_user(data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestListUser:
    def test_if_user_is_authenticated_returns_200(self, authenticate, list_user):
        authenticate(is_superuser=True)
        response = list_user()
        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_not_superuser_returns_403(self, authenticate, list_user):
        authenticate()
        response = list_user()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_not_authenticated_returns_401(self, list_user):
        response = list_user()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestRetrieveUser:
    def test_if_user_is_authenticated_returns_200(self, authenticate, retrieve_user):
        authenticate(is_superuser=True)
        response = retrieve_user()
        assert response.status_code == status.HTTP_200_OK

    def test_if_user_is_not_authenticated_returns_401(self, retrieve_user):
        response = retrieve_user()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_superuser_returns_403(self, authenticate, retrieve_user):
        authenticate()
        response = retrieve_user()
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_not_found_returns_404(self, authenticate, retrieve_user):
        authenticate(is_superuser=True)
        response = retrieve_user(43242)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestRemoveUser:
    def test_if_user_is_authenticated_returns_204(self, authenticate, remove_user):
        authenticate(is_superuser=True)
        response = remove_user()
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_user_is_not_authenticated_returns_401(self, remove_user):
        response = remove_user()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_found_returns_404(self, authenticate, remove_user):
        authenticate(is_superuser=True)
        response = remove_user(43242)
        assert response.status_code == status.HTTP_404_NOT_FOUND
