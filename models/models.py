from sqlalchemy import ForeignKey, Table, MetaData, Column, Integer, String, TIMESTAMP
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


trx_type_table = Table(
    'trx_type',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('type', String, nullable=False, unique=True),
)


money_tx = Table(
    'money',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('type', Integer, ForeignKey('trx_type.id')),
    Column('value', Integer, nullable=False),
    Column('description', String, nullable=True),
    Column('date', TIMESTAMP, default=datetime.datetime.utcnow),
    Column('person', Integer, ForeignKey('Users.id')),
    Column('category', Integer, ForeignKey('category.id'))
)


category_table = Table(
    'category',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, unique= True)
)


money_template_table = Table(
    'template_money',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('Users.id')),
    Column('name', String, nullable=False),
    Column('description', String),
    Column('value', Integer, nullable= False),
    Column('category', Integer, ForeignKey('category.id'))
)

