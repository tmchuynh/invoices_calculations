from sqlalchemy.orm import Mapped, mapped_column

class Author(Base):
    __tablename__ = 'authors'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    
    
    def __init__(self, username, email):
        self.username = username
    
    def __repr__(self):
        return '<User %r>' % self.username