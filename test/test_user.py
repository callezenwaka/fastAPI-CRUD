from src.users.schemas import UserCreateModel

version = 'v1'
users_prefix = f"/api/{version}/users"

def test_create_user(fake_session, fake_user_service, test_client):
    user_data = {
        "email": "spiceowl@mail.com",
        "username": "spiceowl",
        "first_name": "Spice",
        "last_name": "Owl",
        "password": "123456"
    }
    response = test_client.post(
        url=f"{users_prefix}/register",
        json=user_data
    )

    user_data_dict = UserCreateModel(**user_data)

    assert fake_user_service.user_exists_called_once()
    assert fake_user_service.user_exists_called_once_with(user_data['email'], fake_session)
    assert fake_user_service.create_user_called_once()
    assert fake_user_service.create_user_called_once_with(user_data_dict, fake_session)