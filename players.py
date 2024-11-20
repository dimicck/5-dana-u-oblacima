import uuid

# Players database
# The players dictionary stores players' data.
# The key is unique player id (UUID) and the value is a dictionary containing player information:
# player = {
#     "id" - Player's unique UUID (string)
#     "nickname" - Player's nickname (string)
#     "wins" - Number of wins (int)
#     "losses" - Number of losses (int)
#     "elo" - Player's ELO rating (int)
#     "hoursPlayed" - Total hours played (int)
#     "team" - Team the player is assigned to (string or None)
#     "ratingAdjustment" -  adjustment (float or None)
# }

players = {}

def generate_id():
    """
    Generate a unique player ID using UUID.

    :return: A unique player ID.
    :rtype: str
    """

    player_id = str(uuid.uuid4())
    while player_id in players:
        player_id = str(uuid.uuid4())
    return player_id

def nickname_available(nickname):
    """
    Check if nickname is already taken

    :return: Availability status
    :rtype: bool
    """

    for player_id in players:
        if players[player_id]['nickname'] == nickname:
            return False
    return True

def new_player(nickname):
    """
    Create new player object and add it to database.

    :return: Player object
    :rtype: dict
    """
    player = {
        "id": generate_id(),
        "nickname": nickname,
        "wins": 0,
        "losses": 0,
        "elo": 0,
        "hoursPlayed": 0,
        "team": None,
        "ratingAdjustment": None
    }
    players[player['id']] = player
    return player

def create_new_player(nickname):
    """
    Add a new player if the nickname is available.

    :param nickname: Nickname for the new player.
    :type nickname: str
    :return: A dictionary representing the new player if the nickname is available,
             or `None` if the nickname is not available.
    :rtype: dict or None
    """
    if nickname and nickname_available(nickname):
        return new_player(nickname)
    return None

def get_player_by_id(player_id):
    """
    Get a player from the database.

    :param player_id: The UUID of the player
    :type player_id: str
    :return: A dictionary representing the player if player exists, or `None`
    :rtype: dict or None
    """
    if player_id in players:
        return players[player_id]
    return None

def get_all_players():
    """
    :return: A list of dictionaries representing player objects
    :rtype: list
    """
    return [x for x in players.values()]

def set_player_team(player_id, team):
    """
    Set the team for the given player.

    Assign a team to the player with the given player ID;
    Check if the player exists and does not already belong to a team.

    :param player_id: The UUID of the player.
    :type player_id: str
    :param team: The UUID of the team.
    :type team: str
    :return: True if the operation is successful, otherwise False.
    :rtype: bool
    """
    if player_id in players and not players[player_id]['team']:
        players[player_id]['team'] = team
        return True
    return False

def delete_players():
    """
    Delete players from the database.
    """
    players.clear()
