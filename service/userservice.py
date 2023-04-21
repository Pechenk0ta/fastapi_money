from models.models import User_table
from werkzeug.security import generate_password_hash
from sqlalchemy import insert, select


def create_user(db, upload):
    if db.execute(select(User_table.c.id).where(User_table.c.username == upload.username)):
        return "user with this username already exist"
    if not db.execute(select(User_table.c.id).where(User_table.c.email == upload.email)):
        return "user with this email already exist"
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
    user_username = db.execute(
        select(User_table.c.username).where(User_table.c.id == upload.id)
    ).scalar()

    if user_username:
        return user_username

    return None


def update_by_id(db, upload):
    if db.execute(select(User_table.c.username).where(User_table.c.id == upload.id)):
        if (upload.username and upload.email):
            query = db.execute(User_table.update()
                               .where(User_table.c.id == upload.id)
                               .values(username=upload.username, email=upload.email)
                               )
        elif upload.username:
            query = db.execute(User_table.update()
                               .where(User_table.c.id == upload.id)
                               .values(username=upload.username)
                               )
        elif upload.email:
            query = db.execute(User_table.update()
                               .where(User_table.c.id == upload.id)
                               .values(email=upload.email)
                               )
        db.commit()
        return 'good'
    else:
        return 'Id not found'