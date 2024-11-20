import json

import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse, Response

from match import add_new_match
from models import *
from players import create_new_player, get_player_by_id, get_all_players
from team import new_team, get_team_by_id

# pip install -r requirements.txt
app = FastAPI()

@app.post("/players/create")
async def create_player(request: CreatePlayerModel):
    player = create_new_player(request.nickname)
    if player:
        return JSONResponse(content=player)
    raise HTTPException(status_code=400, detail="Player validation failed")

@app.get("/players")
async def get_players():
    players = get_all_players()
    return JSONResponse(content=players)

@app.get("/players/{player_id}")
async def get_player(player_id):
    player = get_player_by_id(player_id)
    if player:
        return JSONResponse(content=player)
    raise HTTPException(status_code=404, detail="Player not found")

@app.post("/teams")
async def create_team(team: CreateTeamModel):
    team = new_team(team.teamName, team.players)
    if team:
        return JSONResponse(content=team)
    raise HTTPException(status_code=400, detail="Team validation failed")

@app.get("/teams/{team_id}")
async def get_team(team_id):
    team = get_team_by_id(team_id)
    if team:
        return Response(content=json.dumps(team), media_type="application/json")
    raise HTTPException(status_code=404, detail="Team not found")

@app.post("/matches")
async def add_match(match: AddMatchModel):
    team1Id, team2Id, winningTeamId, duration = match
    status = add_new_match(team1Id, team2Id, winningTeamId, duration)
    if status:
        return Response()
    raise HTTPException(status_code=400, detail="Match validation failed")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
