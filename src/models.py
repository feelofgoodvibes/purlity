from datetime import datetime
from werkzeug.security import check_password_hash
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import db


class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    urls = relationship("URL", back_populates="user")

    def check_password(self, password):
        return check_password_hash(self.password, password)


class URL(db.Model):
    __tablename__ = "url"

    short_url = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    url = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="urls")
    
    # cascade="all,delete" to delete all visits of URL when URL is deleted
    visits = relationship("Visit", back_populates="url", cascade="all, delete")


class Visit(db.Model):
    __tablename__ = "visit"

    id = Column(Integer, primary_key=True, autoincrement=True)
    short_url = Column(String, ForeignKey("url.short_url"))
    date = Column(DateTime, default=datetime.now)

    url = relationship("URL", back_populates="visits")
