from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from config import DB_USER, DB_PASS, DB_NAME, DB_HOST
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker, Session
from service.userservice import create_user, get_by_id, update_by_id
from schemas.userschema import userCreateSchema, userByIdSchema, userChangeData
from fastapi_jwt_auth import AuthJWT
from schemas.jwt_settings import Settings
from fastapi_jwt_auth.exceptions import AuthJWTException
from schemas.authschema import userLogin
from service.authservice import login_in
from schemas.taskschema import moneycreateschema, money_changes
from service.taskservice import create_money, get_balance, get_balance_by_days
from models.models import category_table

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
session = SessionLocal()


@AuthJWT.load_config
def get_config():
    return Settings()


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


@app.post("/change_data", response_model=str)
async def change_data_view(
        upload: userChangeData,
        db: Session = Depends(get_db)
):
    return update_by_id(db, upload)

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.post('/login')
async def login(upload: userLogin,
                Authorize: AuthJWT = Depends(),
                db: Session = Depends(get_db)
                ):
    return login_in(db, upload, Authorize)


@app.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    Authorize.set_access_cookies(new_access_token)
    return {"msg": "The token has been refresh"}


@app.delete('/logout')
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}


@app.post('/create_task')
async def create_money_tx(upload: moneycreateschema,
                Authorize: AuthJWT = Depends(),
                db: Session = Depends(get_db)):
    return create_money(db, upload, Authorize)


@app.get('/balance')
async def balance(Authorize: AuthJWT = Depends(),
                db: Session = Depends(get_db)):
    return get_balance(db, Authorize)


@app.post('/money_changes_perday')
async def change(upload: money_changes,
                Authorize: AuthJWT = Depends(),
                db: Session = Depends(get_db)
                ):
    return get_balance_by_days(db, Authorize, upload)

