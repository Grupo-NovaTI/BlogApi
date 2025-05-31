from utils.repositories.base_repository import BaseRepository
from users.models.user_model import UserModel as User

class UserRepository(BaseRepository):
    def __init__(self, db_session):
        self.db_session = db_session

    def get_user_by_id(self, user_id: int):
        return self.db_session.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str):
        return self.db_session.query(User).filter(User.username == username).first()

    def create_user(self, user: User):
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def update_user(self, user: User):
        self.db_session.commit()
        return user

    def delete_user(self, user: User):
        self.db_session.delete(user)
        self.db_session.commit()
        
    def get_all_users(self):
        return self.db_session.query(User).all()