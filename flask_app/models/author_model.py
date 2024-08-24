from sqlalchemy.orm import Mapped, mapped_column

class Author(Base):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    
    
    def __init__(self, username, email):
        self.username = username
        self.email = email
    
    def __repr__(self):
        return '<User %r>' % self.username