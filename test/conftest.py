from src.database import get_session
from src.utils.dependency import RoleChecker, AccessTokenBearer, RefreshTokenBearer
from src import app
from unittest.mock import Mock
import pytest
from fastapi.testclient import TestClient

mockSession = Mock()
mockUserService = Mock()
mockBookService = Mock()
accessTokenBearer = AccessTokenBearer()
refreshTokenBearer = RefreshTokenBearer()
roleChecker = RoleChecker('admin')

def get_mock_session():
    yield mockSession

app.dependency_overrides[get_session] = get_mock_session
app.dependency_overrides[accessTokenBearer] = Mock()
app.dependency_overrides[refreshTokenBearer] = Mock()
app.dependency_overrides[roleChecker] = Mock()

@pytest.fixture
def fake_session():
    return mockSession

@pytest.fixture
def fake_user_service():
    return mockUserService

@pytest.fixture
def fake_book_service():
    return mockBookService

@pytest.fixture
def test_client():
    return TestClient(app)