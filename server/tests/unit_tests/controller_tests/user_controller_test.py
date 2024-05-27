#pylint: skip-file
from unittest.mock import patch, MagicMock
from server.src.controllers.user_controller import get_user
from server.src.models.models import User


@pytest.fixture
def app():
    


# These need to be unit tests, mock the response when calling the user stuff

def test_get_user_when_user_exists():
    # Arrange
    mock_user = MagicMock()
    mock_user.to_json.return_value = {"id": 1, "name": "Test User", "email": "test@example.com"}


    with patch('server.src.models.models.User.query.get', return_value = mock_user) as mock_get_user:
        # Act
        response, status_code = get_user(1)
        
        # Assert
        mock_get_user.assert_called_once_with(1)
        assert status_code == 200
        assert response == mock_user.to_json()



def test_get_user_when_user_does_not_exist():
    # Arrange

    # Act

    # Assert

    None