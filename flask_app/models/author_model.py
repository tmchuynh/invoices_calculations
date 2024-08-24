from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_app.models.base_model import Base
from sqlalchemy import String, DateTime, func, PrimaryKeyConstraint, ForeignKey


class Author(Base):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    
    
    def __init__(self, username, email):
        self.username = username
    
    def __repr__(self):
        return '<User %r>' % self.username