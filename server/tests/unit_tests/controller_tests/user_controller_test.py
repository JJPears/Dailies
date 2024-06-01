#pylint: skip-file
import pytest
from unittest.mock import patch, MagicMock
from server.src.controllers.user_controller import get_user
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

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_get_user_when_user_exists(app_context):
    # Arrange
    mock_user = MagicMock()
    mock_user.to_json.return_value = {"id": 1, "name": "Test User", "email": "test@example.com"}

    with patch.object(Query, 'get', return_value = mock_user) as mock_get_user:
        # Act
        response, status_code = get_user(1)
        
        # Assert
        mock_get_user.assert_called_once_with(1)
        assert status_code == 200
        assert response.get_json() == mock_user.to_json()

def test_get_user_when_user_does_not_exist(app_context):
    # Arrange
    expected = jsonify({"error": "User not found"})

    with patch.object(Query, 'get', return_value = None) as mock_get_user:
        # Act
        response, status_code = get_user(1)
        
        # Assert
        mock_get_user.assert_called_once_with(1)
        assert status_code == 404
        assert response.get_json() == expected.get_json()