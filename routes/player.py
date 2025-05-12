from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select, SQLModel
from db.db import get_session, engine
from schemas import player as schema_task
from typing import Annotated, List

from schemas.player import GameSession

router = APIRouter(prefix="/g_sessions", tags=["Управление сессиями в БД"])

@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schema_task.GameSessionCreate,
             summary = 'Добавить сессию')
def create_game(game: Annotated[
                        schema_task.GameSessionCreate, "Описание"
                ],
                session: Session = Depends(get_session)):
    """
    Добавить игровую ссесию.
    """
    new_game = schema_task.GameSession(
        name_game=game.name_game,
        time=game.time,
        date = game.date,
        min_players=game.min_players,
        max_players = game.max_players
    )
    session.add(new_game)
    session.commit()
    session.refresh(new_game)
    return new_game


@router.get("/read", status_code=status.HTTP_200_OK,
 response_model=List[schema_task.GameSessionRead])
def read_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(schema_task.GameSession)).all()
    if tasks is None or len(tasks) == 0:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail=f"The task list is empty."
 )
    return tasks

@router.delete("/{game_id}", status_code=status.HTTP_200_OK)
def delete_task_by_id(game_id: int,
                      session: Session = Depends(get_session)):
    game = session.query(GameSession).filter(GameSession.game_id == game_id).first()
    if game is None:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"Unable to delete task with ID {game_id}: "

    )
    session.delete(game)
    session.commit()
    return {"detail": f"Task with ID {game_id} has been deleted."}

router2 = APIRouter(prefix="/players", tags=["Управление игроками в БД"])

@router2.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schema_task.PlayerCreate,
             summary = 'Добавить игрока')
def create_player(player: Annotated[
                        schema_task.PlayerCreate, "Описание"
                ],
                session: Session = Depends(get_session)):
    """
    Добавить игровую ссесию.
    """
    new_player = schema_task.Players(
        player_name=player.player_name,
        player_email=player.player_email,

    )
    session.add(new_player)
    session.commit()
    session.refresh(new_player)
    return new_player