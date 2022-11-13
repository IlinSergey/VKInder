import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import config


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, unique=True)
    is_favorite = sq.Column(sq.BOOLEAN)
    ban = sq.Column(sq.BOOLEAN)

    def __str__(self):
        return f'Id пользователя: {self.user_id}'

def create_table(engine):
   Base.metadata.create_all(engine)


def record_user(id):
    try:
        engine = sq.create_engine(config.db)
        Session = sessionmaker(bind=engine)
        session = Session()
        user = User(user_id=id)
        session.add(user)
        session.commit()
        session.close()
        return True
    except Exception:
        return False


def show_favorite():
    engine = sq.create_engine(config.db)
    Session = sessionmaker(bind=engine)
    session = Session()
    for user in session.query(User).filter(User.is_favorite == True).all():
        print(user)
    session.commit()
    session.close()


def set_favorite(id_user):
    engine = sq.create_engine(config.db)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(User).filter(User.user_id == id_user).update({'is_favorite': True})
    session.commit()
    session.close()


