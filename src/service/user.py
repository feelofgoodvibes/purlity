from werkzeug.security import generate_password_hash, check_password_hash
from src.models import User
from src.database import SQLAlchemy
from typing import Optional


class UserService():
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all_users(self):
        return User.query.all()

    def get_user(self, user_id: int) -> User:
        user = User.query.filter(User.id==user_id).first()

        if user is None:
            raise ValueError(f"User-{user_id} not found!")

        return user
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        return User.query.filter(User.username==username).first()

    def create_user(self, username: str, password: str) -> User:
        if self.get_user_by_username(username) is not None:
            raise ValueError(f"User with username {username} already exists!")

        new_user = User(username=username, password=generate_password_hash(password))
        self.db.session.add(new_user)

        return new_user

    def update_user(self, user_id: int, password: str) -> User:
        user = self.get_user(user_id)
        user.password = generate_password_hash(password)

        return user

    def delete_user(self, user_id: int) -> User:
        user = self.get_user(user_id)
        self.db.session.delete(user)

        return user
