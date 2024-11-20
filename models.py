from typing import List
from pydantic import BaseModel

# Pydantic models for fastAPI requests

class CreatePlayerModel(BaseModel):
    nickname: str

class CreateTeamModel(BaseModel):
    teamName: str
    players: List[str]

    def __iter__(self):
        return iter((self.teamName, self.players))


class AddMatchModel(BaseModel):
    team1Id: str
    team2Id: str
    winningTeamId: str
    duration: int

    def __iter__(self):
        return iter((self.team1Id, self.team2Id, self.winningTeamId, self.duration))
