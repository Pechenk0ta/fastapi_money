from sqlalchemy import Table, MetaData, Column, Integer, String, TIMESTAMP
import datetime

metadata = MetaData()



User_table = Table(
    'Users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False, unique=True),
    Column('username', String, nullable=False, unique=True),
    Column('password', String, nullable=False),
    Column('registred_at', TIMESTAMP, default=datetime.datetime.utcnow)
)




