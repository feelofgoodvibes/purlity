from werkzeug.security import generate_password_hash, check_password_hash
from src.models import User
from src.database import SQLAlchemy
from typing import Optional


class UserService():
    """This class provides methods for managing user-related operations, such as retrieving, creating, updating, and deleting users."""
    
    def __init__(self, db: SQLAlchemy):
        """Initialize the UserService with a SQLAlchemy instance.

        Args:
            db (SQLAlchemy): An instance of the SQLAlchemy database connection.
        """

        self.db = db

    def get_all_users(self) -> list[User]:
        """Retrieve a list of all users."""

        return User.query.all()

    def get_user(self, user_id: int) -> User:
        """
        Retrieve a user by ID.

        Args:
            user_id (int): ID of the user to retrieve.

        Returns:
            User: The User object associated with the provided user ID.

        Raises:
            ValueError: If the user is not found.
        """

        user = User.query.filter(User.id==user_id).first()

        if user is None:
            raise ValueError(f"User-{user_id} not found!")

        return user
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their username.

        Args:
            username (str): Username of the user to retrieve.

        Returns:
            Optional[User]: The User object associated with the provided username, or None if not found.
        """

        return User.query.filter(User.username==username).first()

    def create_user(self, username: str, password: str) -> User:
        """
        Create a new user with the provided username and hashed password.

        Args:
            username (str): Username for the new user.
            password (str): Password for the new user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the given username already exists.
        """

        if self.get_user_by_username(username) is not None:
            raise ValueError(f"User with username {username} already exists!")

        new_user = User(username=username, password=generate_password_hash(password))
        self.db.session.add(new_user)

        return new_user

    def update_user(self, user_id: int, password: str) -> User:
        """
        Update a user's password by their ID.

        Args:
            user_id (int): ID of the user to update.
            password (str): New password for the user.

        Returns:
            User: The updated User object.

        Raises:
            ValueError: If the user is not found.
        """

        user = self.get_user(user_id)
        user.password = generate_password_hash(password)

        return user

    def delete_user(self, user_id: int) -> User:
        """
        Delete a user by their ID.

        Args:
            user_id (int): ID of the user to delete.

        Returns:
            User: The User object that was deleted.

        Raises:
            ValueError: If the user is not found.
        """

        user = self.get_user(user_id)
        self.db.session.delete(user)

        return user
