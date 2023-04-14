from werkzeug.security import generate_password_hash
from sqlalchemy import select
from models.models import User_table

def login_in(db, upload, Authorize):
    if db.execute(select(User_table).where(
            (User_table.c.username == upload.username) &
            (User_table.c.password == generate_password_hash(upload.password))
                    )):
        access_token = Authorize.create_access_token(subject=upload.username)
        refresh_token = Authorize.create_refresh_token(subject=upload.username)
        Authorize.set_access_cookies(access_token)
        Authorize.set_refresh_cookies(refresh_token)
        return {"msg": "Successfully login"}
    else:
        return {"msg": "Unsuccess"}