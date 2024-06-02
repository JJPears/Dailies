#pylint: skip-file
import pytest
from unittest.mock import patch, MagicMock
from server.src.controllers.user_controller import get_user, create_user
from server.src.models.models import User
from server.src.app import create_app
from server.src.database import db
from sqlalchemy.orm import Query
from flask import jsonify


@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": 'sqlite:///:memory:',  # use an in-memory SQLite database
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }

    app = create_app(test_config)  # pass test configuration

    with app.app_context():
        db.create_all()

    yield app  # yield the app context for tests

    with app.app_context():
        db.drop_all()  # clean up after tests

@pytest.fixture
def app_context(app):
    with app.app_context():
        yield

@pytest.fixture()
def client(app):
    return app.test_client()

def test_get_user_when_user_exists(app_context, client):
    # Arrange
    mock_user = MagicMock()
    mock_user.to_json.return_value = {"id": 1, "name": "Test User", "email": "test@example.com"}

    with patch.object(Query, 'get', return_value = mock_user) as mock_get_user:
        # Act
        response = client.get("/user/1")
        
        # Assert
        mock_get_user.assert_called_once_with(1)
        assert response.status_code == 200
        assert response.get_json() == mock_user.to_json()

def test_get_user_when_user_does_not_exist(app_context, client):
    # Arrange
    expected = {"error": "User not found"}

    with patch.object(Query, 'get', return_value = None) as mock_get_user:
        # Act
        response = client.get("/user/1")
        
        # Assert
        mock_get_user.assert_called_once_with(1)
        assert response.status_code == 404
        assert response.get_json() == expected

def test_create_user_should_return_201_when_user_is_created(app_context, client):
    # Arrange
    mock_user = MagicMock()
    mock_user.to_json.return_value = {"id": 1, "name": "Test User", "email": "test@example.com"}
    user_data = {"name": "Test User", "email": "test@example.com"}
    with patch.object(User, 'create', return_value = mock_user) as mock_create_user:
        # Act
        response = client.post("/user", json=user_data, content_type='application/json')

        # Assert
        mock_create_user.assert_called_once_with(user_data)
        assert response.status_code == 201
        assert response.get_json() == mock_user.to_json()

def test_create_user_should_return_400_when_no_data_is_provided(app_context, client):
    # Arrange
    expected = {"error": "No data provided for creating user"}

    # Act
    response = client.post("/user", json={}, content_type='application/json')

    # Assert
    assert response.status_code == 400
    assert response.get_json() == expected

def test_create_user_should_return_400_when_user_data_is_invalid(app_context, client):
    # Arrange
    expected = {"error": "Invalid user data"}

    with patch.object(User, 'create', side_effect = ValueError("Invalid user data")) as mock_create_user:
        # Act
        response = client.post("/user", json={"name": "Test User"}, content_type='application/json')

        # Assert
        mock_create_user.assert_called_once()
        assert response.status_code == 400
        assert response.get_json() == expected

