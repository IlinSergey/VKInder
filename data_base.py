import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

import config


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = sq.Column(sq.Integer)
    user_id = sq.Column(sq.Integer, primary_key=True)
    is_favorite = sq.Column(sq.BOOLEAN)
    customer_id = sq.Column(sq.Integer, primary_key=True)
    ban = sq.Column(sq.BOOLEAN)

    def __str__(self):
        return f'Id пользователя: {self.user_id}'


def create_table(engine):
    Base.metadata.create_all(engine)


def record_user(id, customer_id):
    """Заносит порльзователя в БД и возвращает True в случае успеха, если такой ID уже есть в базе, возвращает False"""
    try:
        engine = sq.create_engine(config.db)
        Session = sessionmaker(bind=engine)
        session = Session()
        create_table(engine)
        user = User(user_id=id, customer_id=customer_id)
        session.add(user)
        session.commit()
        session.close()
        return True
    except Exception:
        return False


def show_favorite(cusromer_id):
    """Функция возвращает список ID пользователей, которые добавлены в список 'Избранные'"""
    engine = sq.create_engine(config.db)
    Session = sessionmaker(bind=engine)
    session = Session()
    users_list = []
    for user in session.query(User).filter(User.is_favorite == True, User.customer_id == cusromer_id).all():
        users_list.append(user.user_id)
    session.commit()
    session.close()
    return users_list


def set_favorite(id_user, customer_id):
    """Уствнавливает значение True в столбце 'is_vavorite' у пользователя с заданным ID"""
    engine = sq.create_engine(config.db)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(User).filter(User.user_id == id_user).update({'is_favorite': True})
    session.query(User).filter(User.user_id == id_user).update({'customer_id': customer_id})
    session.commit()
    session.close()
