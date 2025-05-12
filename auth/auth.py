from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session , select
from auth import auth_handler
from db.db import get_session
from schemas import player as schema_task
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

router = APIRouter(prefix="/auth", tags=["Безопасность"])

@router.post("/signup", status_code=status.HTTP_201_CREATED,
             response_model=int,
             summary = 'Добавить пользователя')
def create_user(user: schema_task.Players,
                session: Session = Depends(get_session)):
    new_user = schema_task.Players(
        player_name=user.player_name,
        player_email=user.player_email,
        player_password= user.player_password
    )
    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user.player_id
    except IntegrityError as e:
        assert isinstance(e.orig, UniqueViolation)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"User with email {user.player_email} already exists"
        )

@router.post("/login", status_code=status.HTTP_200_OK,
             summary = 'Войти в систему')
def user_login(login_attempt_data: OAuth2PasswordRequestForm = Depends(),
               db_session: Session = Depends(get_session)):
    statement = (select(schema_task.Players)
                 .where(schema_task.Players.player_email == login_attempt_data.username))
    existing_user = db_session.exec(statement).first()

    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User {login_attempt_data.username} not found"
        )
    if existing_user.player_password == login_attempt_data.password:
        access_token = auth_handler.create_token(existing_user.player_id)
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Wrong password for user {login_attempt_data.username}"
        )



