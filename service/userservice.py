from models.users import User_table
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session
from schemas.userschema import userCreateSchema
from sqlalchemy import insert, select


def create_user(db: Session, upload: userCreateSchema):
    comm = insert(User_table).values(
        username=upload.username,
        email=upload.email,
        password=generate_password_hash(upload.password)
    )
    db.execute(comm)
    db.commit()

    user_id = db.execute(
        select(User_table.c.id).where(User_table.c.username == upload.username)
    ).scalar()

    return user_id

def get_by_id (db, upload):
    print(upload.id, type(upload.id))
    user_username = db.execute(
        select(User_table.c.username).where(User_table.c.id == upload.id)
    ).scalar()

    return user_username