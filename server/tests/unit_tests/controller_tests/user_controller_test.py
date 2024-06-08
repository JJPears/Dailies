#pylint: skip-file
import pytest
from unittest.mock import patch, MagicMock
from server.src.controllers.user_controller import get_user, create_user
from server.src.models.models import User, Habit
from server.src.app import create_app
from server.src.database import db
from werkzeug.exceptions import BadRequest, NotFound


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

    with patch.object(User, 'query') as mock_query:
        mock_query.get.return_value = mock_user
        # Act
        response = client.get("/user/1")
        
        # Assert
        mock_query.get.assert_called_once_with(1)
        assert response.status_code == 200
        assert response.get_json() == mock_user.to_json()

def test_get_user_when_user_does_not_exist(app_context, client):
    # Arrange
    expected = {"error": "User not found"}

    with patch.object(User, 'query') as mock_query:
        mock_query.get.return_value = None
        # Act
        response = client.get("/user/1")
        
        # Assert
        mock_query.get.assert_called_once_with(1)
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
    expected = {"error": "No user data provided"}

    # Act
    response = client.post("/user", json={}, content_type='application/json')

    # Assert
    assert response.status_code == 400
    assert response.get_json() == expected

def test_create_user_should_return_400_when_user_data_is_invalid(app_context, client):
    # Arrange
    expected = {"error": "Missing mandatory fields: email, password"}

    with patch.object(User, 'create', side_effect = BadRequest("Missing mandatory fields: email, password")) as mock_create_user:
        # Act
        response = client.post("/user", json={"name": "Test User"}, content_type='application/json')

        # Assert
        mock_create_user.assert_called_once()
        assert response.status_code == 400
        assert response.get_json() == expected


def test_update_user_should_return_201_when_user_is_updated(app_context, client):
    # Arrange
    mock_user = MagicMock()
    mock_user.to_json.return_value = {"id": 1, "name": "Test User", "email": "test@example.com"}
    user_data = {"name": "Updated user", "email": "test@example.com"}
    with patch.object(User, 'query') as mock_query:
        mock_query.get.return_value = mock_user

        with patch.object(mock_user, 'update', return_value = None) as mock_update_user:
            # Act
            response = client.put("/user/1", json=user_data, content_type='application/json')

            # Assert
            mock_query.get.assert_called_once_with(1)
            mock_update_user.assert_called_once_with(user_data)
            assert response.status_code == 201
            assert response.get_json() == mock_user.to_json()

def test_update_user_should_return_400_when_no_user_data_is_provided(app_context, client):
    # Arrange
    expected = {"error": "No user data provided"}

    # Act
    response = client.put("/user/1", json={}, content_type='application/json')

    # Assert
    assert response.status_code == 400
    assert response.get_json() == expected


def test_update_user_should_return_404_when_user_not_found(app_context, client):
    # Arrange
    mock_user = MagicMock()
    mock_user.to_json.return_value = {"id": 1, "name": "Test User", "email": "test@example.com"}
    user_data = {"name": "Updated user", "email": "test@example.com"}
    expected = {"error": "User not found"}
    with patch.object(User, 'query') as mock_query:
        mock_query.get.return_value = None

        # Act
        response = client.put("/user/1", json=user_data, content_type='application/json')

        # Assert
        mock_query.get.assert_called_once_with(1)
        assert response.status_code == 404
        assert response.get_json() == expected


def test_create_habit_should_return_201_when_habit_is_created(app_context, client):
    # Arrange
    mock_habit = MagicMock()
    mock_habit.to_json.return_value = {"id": 1, "name": "Test Habit", "user_id": 1}
    habit_data = {"name": "Test Habit"}
    with patch.object(Habit, 'create', return_value=mock_habit) as mock_create_habit:
        # Act
        response = client.post("/user/1/habit", json=habit_data, content_type='application/json')
        # Assert
        mock_create_habit.assert_called_once_with(habit_data, 1)
        assert response.status_code == 201
        assert response.get_json() == mock_habit.to_json()

def test_create_habit_should_return_404_when_user_not_found(app_context, client):
    # Arrange
    expected = {"error": "User not found"}
    habit_data = {"name": "Test Habit"}
    with patch.object(Habit, 'create', side_effect=NotFound("User not found")) as mock_create_habit:
        # Act
        response = client.post("/user/1/habit", json=habit_data, content_type='application/json')
        # Assert
        mock_create_habit.assert_called_once_with(habit_data, 1)
        assert response.status_code == 404
        assert response.get_json() == expected


def test_create_habit_should_return_400_when_no_data_is_provided(app_context, client):
    # Arrange
    expected = {"error": "No habit data provided"}
    # Act
    response = client.post("/user/1/habit", json={}, content_type='application/json')
    # Assert
    assert response.status_code == 400
    assert response.get_json() == expected

def test_create_habit_should_return_400_when_habit_data_is_invalid(app_context, client):
    # Arrange
    expected = {"error": "Invalid habit data"}
    with patch.object(Habit, 'create', side_effect=BadRequest("Invalid habit data")) as mock_create_habit:
        # Act
        response = client.post("/user/1/habit", json={"name": "Test Habit"}, content_type='application/json')
        # Assert
        mock_create_habit.assert_called_once()
        assert response.status_code == 400
        assert response.get_json() == expected

def test_create_habit_should_return_400_when_sql_alechemy_error_occurs(app_context, client):
    # Arrange
    expected = {"error": "An error occurred while creating habit for user 1"}
    with patch.object(Habit, 'create', side_effect=BadRequest("An error occurred while creating habit for user 1")) as mock_create_habit:
        # Act
        response = client.post("/user/1/habit", json={"name": "Test Habit"}, content_type='application/json')
        # Assert
        mock_create_habit.assert_called_once()
        assert response.status_code == 400
        assert response.get_json() == expected

def test_update_habit_should_return_201_when_habit_is_updated(app_context, client):
    # Arrange
    mock_user = MagicMock()
    mock_habit = MagicMock()
    mock_habit.to_json.return_value = {"id": 1, "name": "Test Habit", "user_id": 1}
    habit_data = {"name": "Updated Habit"}
    with patch.object(User, 'query') as mock_user_query:
        mock_user_query.get.return_value = mock_user
        with patch.object(Habit, 'query') as mock_habit_query:
            mock_habit_query.get.return_value = mock_habit
            with patch.object(mock_habit, 'update', return_value = None) as mock_update_habit:
                # Act
                response = client.put("/user/1/habit/1", json=habit_data, content_type='application/json')

                # Assert
                mock_user_query.get.assert_called_once_with(1)
                mock_habit_query.get.assert_called_once_with(1)
                mock_update_habit.assert_called_once_with({"name": "Updated Habit"})
                assert response.status_code == 201

def test_update_habit_should_return_400_when_no_habit_data_is_provided(app_context, client):
    # Arrange
    expected = {"error": "No habit data provided"}
    # Act
    response = client.put("/user/1/habit/1", json={}, content_type='application/json')
    # Assert
    assert response.status_code == 400
    assert response.get_json() == expected

def test_update_habit_should_return_404_when_user_not_found(app_context, client):
    # Arrange
    expected = {"error": "User not found"}
    habit_data = {"name": "Updated Habit"}
    with patch.object(User, 'query') as mock_user_query:
        mock_user_query.get.return_value = None
        # Act
        response = client.put("/user/1/habit/1", json=habit_data, content_type='application/json')
        # Assert
        mock_user_query.get.assert_called_once_with(1)
        assert response.status_code == 404
        assert response.get_json() == expected

def test_update_habit_should_return_404_when_habit_not_found(app_context, client):
    # Arrange
    mock_user = MagicMock()
    expected = {"error": "Habit not found"}
    habit_data = {"name": "Updated Habit"}
    with patch.object(User, 'query') as mock_user_query:
        mock_user_query.get.return_value = mock_user
        with patch.object(Habit, 'query') as mock_habit_query:
            mock_habit_query.get.return_value = None
            # Act
            response = client.put("/user/1/habit/1", json=habit_data, content_type='application/json')
            # Assert
            mock_user_query.get.assert_called_once_with(1)
            mock_habit_query.get.assert_called_once_with(1)
            assert response.status_code == 404
            assert response.get_json() == expected