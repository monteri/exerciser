from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import Client

import pytest

from pdp.api.services.token_utils import create_tokens


@pytest.fixture()
def anonymous_client():
    return Client()


@pytest.fixture
def user():
    # Hash the password
    hashed_password = make_password("password123")
    # Create a user for testing with the hashed password
    user = User.objects.create(username="testuser", password=hashed_password)
    return user


@pytest.fixture
def auth_client(user):
    client = Client()
    access_token, refresh_token = create_tokens(user.id)
    # Set the access token in the 'Authorization' header for future requests
    client.headers = {"Authorization": f"Bearer {access_token}"}

    return client
