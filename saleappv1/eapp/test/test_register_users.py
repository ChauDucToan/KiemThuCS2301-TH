import pytest
from eapp.test.test_base import create_app, test_app, test_session
from eapp import db
from eapp.dao import add_user
from eapp.models import User
import hashlib

@pytest.fixture
def mock_cloudinary(monkeypatch):
    def fake_image(file):
        return {'secure_url': "https://hello.png"}
    monkeypatch.setattr('cloudinary.uploader.upload', fake_image)

def test_add_user(test_session):
    name = "abcd"
    username = "tester"
    password = "Admin@123"

    add_user(name=name, username=username, password=password, avatar=None)

    u = User.query.filter(username.__eq__(username)).first()
    assert u
    assert u.name == name
    assert u.username == username
    assert u.password == str(hashlib.md5(password.encode('utf-8')).hexdigest())

def test_existed_user(test_session):
    name = "abcd"
    username = "tester"
    password = "Admin@123"

    add_user(name=name, username=username, password=password, avatar=None)
    with pytest.raises(ValueError):
        add_user(name=name, username=username, password=password, avatar=None)

def test_avatar(test_session, mock_cloudinary):
    name = "abcd"
    username = "tester"
    password = "Admin@123"

    add_user(name=name, username=username, password=password, avatar="aaaaa")

    u = User.query.filter(username.__eq__(username)).first()
    assert u
    assert u.avatar == "https://hello.png"