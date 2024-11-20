import uuid
from players import get_player_by_id, set_player_team

# Number of players in a team
TEAM_SIZE = 5

# Teams database
# The key is unique team id (UUID) and the value is a dictionary containing team information:
# team = {
#     "id" - Player's unique UUID (string)
#     "teamname" - Team name (string)
#     "players" - List of dictionaries representing players in a team (List)
# }
teams = {}

def generate_team_id():
    """
    Generate a unique team ID using UUID

    :return: A unique team ID
    :rtype: str
    """
    team_id = str(uuid.uuid4())
    while team_id in teams:
        team_id = str(uuid.uuid4())
    return team_id

def teamname_available(team_name):
    """
    Checks if the given team name is not taken.

    :param str team_name: The name of the team to check.
    :return: True if the team name is available, False otherwise.
    :rtype: bool
    """
    for team_id in teams:
        if teams[team_id]['teamName'] == team_name:
            return False
    return True

def new_team(team_name, players):
    """
    Add a new team to the database

    Functions ensures that:
    - Team name is available
    - There are exactly 5 players in the team
    - No player already has a team

    :param str team_name: The name of the team.
    :param list players: A list of player IDs to form the team.
    :return: The created team dictionary, or None if arguments are not valid.
    :rtype: dict or None
    """
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
    """
    Get team information by given team ID.

    :param str team_id: The unique ID of the team.
    :return: The team dictionary, or None if not found.
    :rtype: dict or None
    """
    if team_id in teams:
        return teams[team_id]
    return None

def average_team_elo(team_id):
    """
    Calculates the average ELO rating for a team.

    :param str team_id: The unique ID of the team.
    :return: The average ELO rating of the team.
    :rtype: float
    """
    avg = 0
    for player in teams[team_id]['players']:
        avg += player['elo']
    return avg / TEAM_SIZE

def delete_teams():
    """
    Delete players from the database.
    """
    teams.clear()