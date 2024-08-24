from sqlalchemy.orm import Mapped, mapped_column
from flask_app.models.base_model import Base
from sqlalchemy import String, DateTime, func, PrimaryKeyConstraint, ForeignKey


class Book(Base):
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(primary_key=True)
    published: Mapped[bool] = mapped_column(primary_key=False, default=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('author.id'), nullable=False)
    author: Mapped['Author'] = relationship('Author', back_populates='books')
    
    def __init__(self, title, author_id, author):
        self.title = title
        self.author = author
        self.published = published
    