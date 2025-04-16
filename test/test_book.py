# from src.books.schemas import UserCreateModel

version = 'v1'
books_prefix = f"/api/{version}/books"

def test_get_all_books(fake_session, fake_book_service, test_client):
    response = test_client.get(
        url=f"{books_prefix}",
    )

    assert fake_book_service.user_exists_called_once()
    assert fake_book_service.user_exists_called_once_with(fake_session)
    # assert fake_book_service.create_user_called_once()
    # assert fake_book_service.create_user_called_once_with(user_data_dict, fake_session)