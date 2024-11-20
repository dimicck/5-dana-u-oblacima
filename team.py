import uuid
from players import get_player_by_id, set_player_team

TEAM_SIZE = 5

teams = {}

def generate_team_id():
    team_id = str(uuid.uuid4())
    while team_id in teams:
        team_id = str(uuid.uuid4())
    return team_id

def teamname_available(teamName):
    for team_id in teams:
        if teams[team_id]['teamName'] == teamName:
            return False
    return True

def new_team(team_name, players):
    # players = list of player_ids

    if not teamname_available(team_name) or len(players) != TEAM_SIZE:
        return None

    players_info = []
    team_id = generate_team_id()

    for id in players:
        if not set_player_team(id, team_id):
            return None
        players_info.append(get_player_by_id(id))

    team = {
        "id": team_id,
        "teamName": team_name,
        "players": players_info
    }
    teams[team_id] = team
    return team

def get_team_by_id(team_id):
    if team_id in teams:
        return teams[team_id]
    return None

def average_team_elo(team_id):
    avg = 0
    for player in teams[team_id]['players']:
        avg += player['elo']
    return avg / TEAM_SIZE

def delete_teams():
    teams.clear()