import pytest
from flask import Flask

from flask_login import login_user

from application import app

from application import models


@pytest.fixture
def client():
    
    app.testing = True
    app.config['TESTING'] = True
    return app.test_client()


@pytest.fixture
def login_for_test(client):
   
    client.post('/login', data=dict(
        name="Yura_3",
        password=1111
    ), follow_redirects=True)  


@pytest.fixture
def test_app():
    return app

