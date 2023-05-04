from werkzeug.security import generate_password_hash, check_password_hash
from src.models import User
from src.database import SQLAlchemy
from typing import Union

class UserService():
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all_users(self):
        return User.query.all()

    def get_user(self, user_id: int) -> Union[User, None]:
        user = User.query.filter(User.id==user_id).first()

        if user is None:
            raise ValueError(f"User-{user_id} not found!")

        return user

    def create_user(self, username: str, password: str) -> User:
        new_user = User(username=username, password=generate_password_hash(password))
        self.db.session.add(new_user)

        return new_user

    def update_user(self, user_id: int, password: str) -> Union[User, None]:
        user = self.get_user(user_id)
        user.password = generate_password_hash(password)

        return user

    def delete_user(self, user_id: int) -> Union[User, None]:
        user = self.get_user(user_id)
        self.db.session.delete(user)

        return user
