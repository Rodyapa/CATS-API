import uuid

import pytest
from rest_framework.test import APIClient

'''
Fixtures of this file are used among the all test modules.
'''


@pytest.fixture
def api_client():
    '''Return Anonymous API Client'''
    return APIClient()


@pytest.fixture
def test_password():
    'Return password'
    return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    '''Return new user instance'''
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        user = django_user_model.objects.create_user(**kwargs)
        return user
    return make_user


@pytest.fixture
def auto_login_user(db, api_client, create_user, test_password):
    '''Return Authenticated client and User'''
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        api_client.login(username=user.username, password=test_password)
        return api_client, user
    return make_auto_login


@pytest.fixture
def api_client_with_credentials(db, create_user, api_client):
    '''Return Authenticated client with Token and User'''
    def make_client():
        user = create_user(is_staff=False)
        api_client.force_authenticate(user=user)
        return api_client
    return make_client()


@pytest.fixture
def api_staff_client_with_credentials(db, create_user, api_client):
    '''Return Authenticated Staff client with Token and User'''
    def make_client():
        user = create_user(is_staff=True)
        api_client.force_authenticate(user=user)
        return api_client
    return make_client()
