from pydantic import BaseModel

from server.utils import Time

class Achievement(BaseModel):
    key: str
    is_achieved: bool
    unlock_time: Time

class PlayerGameAchievements(BaseModel):
    steam_id: str
    game_name: str
    completion: float
    achievements: list[Achievement]
