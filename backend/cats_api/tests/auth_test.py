import pytest


@pytest.fixture
def user_tokens(api_client, create_user, test_password):
    '''Log in the user and store the refresh token.'''
    # Arrange
    url = '/api/auth/jwt/create/'
    create_user()
    user_credentials = {
        'username': 'username',
        'password': test_password,
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


@pytest.mark.django_db
def test_token_create(api_client, create_user, test_password):
    '''Test JWT token creation.'''
    # Arrange
    url = '/api/auth/jwt/create/'
    create_user()
    user_credentials = {
        'username': 'username',
        'password': test_password,
    }
    # Act
    response = api_client.post(url, user_credentials)
    # Assert
    assert response.status_code == 200
    assert 'access' in response.data, 'Response must contain access token'
    assert 'refresh' in response.data, 'Response must contain refresh token'


@pytest.mark.django_db
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


@pytest.mark.django_db
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
