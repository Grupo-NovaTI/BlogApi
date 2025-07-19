from test import BlogModel, CommentModel, TagModel, UserModel, UserRepository
from typing import List, Optional

import pytest
from sqlalchemy.orm.session import Session
from test.utils.utils import db_session


@pytest.fixture(scope="function")
def user_repo(db_session: Session) -> UserRepository:
    return UserRepository(db_session=db_session)

class TestUserRepository:
    def test_create_user(self, user_repo: UserRepository, db_session: Session) -> None:
        # Arrange
        new_user = UserModel(username="testuser", email="test@example.com", name="Test", last_name="User", hashed_password="hashedpassword")
        # Act
        created_user: UserModel = user_repo.create_user(new_user)
        db_session.commit()
        
        # Assert
        assert created_user.id is not None
        assert created_user.username == "testuser" # type: ignore
        assert created_user.email == "test@example.com" # type: ignore
        assert created_user.name == "Test" # type: ignore
        assert created_user.last_name == "User" # type: ignore
        assert created_user.hashed_password == "hashedpassword" # type: ignore

    def test_get_user_by_id(self, user_repo: UserRepository, db_session: Session) -> None:
        # Arrange
        user = UserModel(username="get_id_user", email="getid@example.com", name="Get", last_name="ID", hashed_password="hashedpassword")
        db_session.add(user)
        db_session.commit()
        # Act
        found_user: Optional[UserModel] = user_repo.get_user_by_id(user.id) # type: ignore
        # Assert
        assert found_user is not None
        assert found_user.id == user.id # type: ignore
        assert found_user.username == "get_id_user" # type: ignore
        assert found_user.email == "getid@example.com" # type: ignore
        assert found_user.name == "Get" # type: ignore
        assert found_user.last_name == "ID" # type: ignore  
        assert found_user.hashed_password == "hashedpassword" # type: ignore
        
    def test_get_user_by_id_not_found(self, user_repo: UserRepository) -> None:
        # Act
        found_user: Optional[UserModel] = user_repo.get_user_by_id(user_id=999)
        # Assert
        assert found_user is None

    def test_get_user_by_username(self, user_repo: UserRepository, db_session: Session) -> None:
        # Arrange
        user = UserModel(username="findme", email="findme@example.com", name="Find", last_name="Me", hashed_password="hashedpassword")
        db_session.add(user)
        db_session.commit()
        # Act
        found_user: Optional[UserModel] = user_repo.get_user_by_username("findme")
        # Assert
        assert found_user is not None
        assert found_user.username == "findme" # type: ignore
        assert found_user.email == "findme@example.com" # type: ignore
        assert found_user.name == "Find" # type: ignore
        assert found_user.last_name == "Me" # type: ignore
        assert found_user.hashed_password == "hashedpassword" # type: ignore

    def test_get_user_by_email(self, user_repo: UserRepository, db_session: Session) -> None:
        # Arrange
        user: UserModel = UserModel(username="testemail", email="findby@email.com", name="Find", last_name="ByEmail", hashed_password="hashedpassword")
        db_session.add(user)
        db_session.commit()
        # Act
        found_user: Optional[UserModel] = user_repo.get_user_by_email("findby@email.com")
        # Assert
        assert found_user is not None
        assert found_user.username == "testemail" # type: ignore
        assert found_user.id is not None
        assert found_user.name == "Find" # type: ignore
        assert found_user.last_name == "ByEmail" # type: ignore
        assert found_user.hashed_password == "hashedpassword" # type: ignore
        assert found_user.email == "findby@email.com" # type: ignore

    def test_get_user_by_email_or_username(self, user_repo: UserRepository, db_session: Session) -> None:
        # Arrange
        user = UserModel(username="eitheror", email="eitheror@example.com", name="Either", last_name="Or", hashed_password="hashedpassword")
        db_session.add(user)
        db_session.commit()
        # Act
        found_by_username: Optional[UserModel] = user_repo.get_user_by_email_or_username(email="wrong@email.com", username="eitheror")
        # Assert
        assert found_by_username is not None
        assert found_by_username.id == user.id # type: ignore
        assert found_by_username.username == "eitheror" # type: ignore
        assert found_by_username.email == "eitheror@example.com" # type: ignore
        assert found_by_username.name == "Either" # type: ignore
        assert found_by_username.last_name == "Or" # type: ignore
        
        found_by_email: Optional[UserModel] = user_repo.get_user_by_email_or_username(email="eitheror@example.com", username="wronguser")
        assert found_by_email is not None
        assert found_by_email.id == user.id # type: ignore
        assert found_by_email.username == "eitheror" # type: ignore
        assert found_by_email.email == "eitheror@example.com" # type: ignore
        assert found_by_email.name == "Either" # type: ignore
        assert found_by_email.last_name == "Or" # type: ignore

    def test_update_user(self, user_repo: UserRepository, db_session: Session) -> None:
        # Arrange
        user = UserModel(username="original", email="original@example.com", name="Original", last_name="User", hashed_password="hashedpassword")
        db_session.add(user)
        db_session.commit()
        # Act
        user_to_update: Optional[UserModel] = user_repo.get_user_by_id(user.id) # type: ignore
        update_data: dict[str, str] = {"username": "updated", "email": "updated@example.com"}
        updated_user: Optional[UserModel] = user_repo.update_user(user_to_update, update_data)
        db_session.commit()
        # Assert
        assert updated_user.username == "updated" # type: ignore
        assert updated_user.email == "updated@example.com" # type: ignore
        assert updated_user.name == "Original" # type: ignore
        assert updated_user.last_name == "User" # type: ignore
        refreshed_user: Optional[UserModel] = user_repo.get_user_by_id(user.id) # type: ignore
        assert refreshed_user is not None
        assert refreshed_user.username == "updated" # type: ignore
        assert refreshed_user.email == "updated@example.com" # type: ignore
        assert refreshed_user.name == "Original" # type: ignore
        assert refreshed_user.last_name == "User" # type: ignore

    def test_delete_user(self, user_repo: UserRepository, db_session: Session) -> None:
        # Arrange
        user_to_delete = UserModel(username="deleteme", email="deleteme@example.com", name="Delete", last_name="Me", hashed_password="hashedpassword")
        db_session.add(user_to_delete)
        db_session.commit()
        
        assert user_repo.get_user_by_id(user_to_delete.id) is not None # type: ignore
        # Act
        user_repo.delete_user(user_to_delete)
        db_session.commit()
        # Assert
        assert user_repo.get_user_by_id(user_to_delete.id) is None # type: ignore

    def test_get_all_users_with_pagination(self, user_repo: UserRepository, db_session: Session) -> None:
        # Arrange
        for i in range(5):
            user = UserModel(username=f"user{i}", email=f"user{i}@example.com", name=f"User{i}", last_name=f"Last{i}", hashed_password="hashedpassword")
            db_session.add(user)
        db_session.commit()
        # Act & Assert
        first_page: List[UserModel] = user_repo.get_all_users(offset=0, limit=3)
        assert len(first_page) == 3
        assert first_page[0].username == "user0" # type: ignore
        assert first_page[2].username == "user2" # type: ignore

        second_page: List[UserModel] = user_repo.get_all_users(offset=3, limit=3)
        assert len(second_page) == 2
        assert second_page[0].username == "user3" # type: ignore
        assert second_page[1].username == "user4" # type: ignore