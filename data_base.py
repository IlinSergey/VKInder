import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import config


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, unique=True)
    is_favorite = sq.Column(sq.BOOLEAN)

    def __str__(self):
        return f'Id пользователя: {self.user_id}'

def create_table(engine):
   Base.metadata.create_all(engine)
