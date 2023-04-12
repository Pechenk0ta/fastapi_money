from fastapi import FastAPI, Depends, requests
from config import DB_USER, DB_PASS, DB_NAME, DB_HOST
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session
from service.userservice import create_user, get_by_id
from schemas.userschema import userCreateSchema, userByIdSchema


SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
session = SessionLocal()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/register", response_model= dict)
async def create_user_view(
        upload:userCreateSchema,
        db: Session = Depends(get_db)
):
    user_id = create_user(db, upload)
    return {'user_id':user_id}

@app.post("/get_by_id", response_model=dict)
async def user_by_id_view(
        upload: userByIdSchema,
        db: Session = Depends(get_db)
):
    username = get_by_id(db, upload)
    return {"username":username}
