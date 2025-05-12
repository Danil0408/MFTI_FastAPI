from pydantic import BaseModel
from datetime import date, time
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field as SQLField

class PlayerCreate(BaseModel):
    player_name: str
    player_email: str
    player_password: str

class PlayerRead(PlayerCreate):
    player_id : int

class GameSessionCreate(BaseModel):
    name_game : str
    date : date
    time : time
    min_players : int
    max_players : int


class GameSessionRead(GameSessionCreate):
    game_id : int

class GameSession(SQLModel, table=True):
    game_id: int = SQLField(default=None, nullable=False, primary_key=True)
    date: date
    name_game : str
    time : time
    min_players : int
    max_players : int

class Players(SQLModel, table = True):
    __table_args__ = (UniqueConstraint("player_email"),)
    player_id: int = SQLField(default=None, nullable=False, primary_key=True)
    player_name : str
    player_email: str  = SQLField(nullable=True, unique_items=True)
    player_password: str