import sqlalchemy
from sqlalchemy import *
import config



meta = MetaData()

users = Table('Users', meta,
              Column('id', Integer, primary_key=True),
              Column('user_id', Integer, nullable=False, unique=True)
               )


engine = sqlalchemy.create_engine(config.db)
meta.create_all(engine)

connection = engine.connect()

try:
    connection.execute(users.insert().values(user_id='16'))
except:
    print('Такой пользователь уже был')
result = connection.execute(select(users))


connection.close()