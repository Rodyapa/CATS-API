import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_tokens(api_client):
    '''Log in the user and store the refresh token.'''
    # Arrange
    url = '/api/auth/jwt/create/'
    user_credentials = {
        'username': 'username',
        'password': 'Strong_password1',
    }
    # Act
    response = api_client.post(url, user_credentials)
    # Assert
    assert response.status_code == 200
    access_token = response.data.get('access')
    refresh_token = response.data.get('refresh')
    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def test_token_create(api_client):
    '''Test JWT token creation.'''
    # Arrange
    url = '/api/auth/jwt/create/'
    user_credentials = {
        'username': 'username',
        'password': 'Strong_password1',
    }
    # Act
    response = api_client.post(url, user_credentials)
    # Assert
    assert response.status_code == 200
    assert 'access' in response.data, 'Response must contain access token'
    assert 'refresh' in response.data, 'Response must contain refresh token'


def test_token_refresh(api_client, user_tokens):
    '''Test refreshing the JWT token.'''
    # Arrange
    url = '/api/auth/jwt/refresh/'
    refresh_token_data = {
        'refresh': user_tokens['refresh_token']
    }
    # Act
    response = api_client.post(url, refresh_token_data)
    # Assert
    assert response.status_code == 200
    assert 'access' in response.data, 'Response must contain access token'


def test_token_verify(api_client, user_tokens):
    '''Test verifying the JWT token.'''
    # Arrange
    url = '/api/auth/jwt/verify/'
    token_data = {
        'token': user_tokens['access_token']
    }
    # Act
    response = api_client.post(url, token_data)
    # Assert
    assert response.status_code == 200
