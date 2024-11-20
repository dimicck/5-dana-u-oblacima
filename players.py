import uuid

players = {}
# Players database
# key = PlayerId, value = player object

def generate_id():
    player_id = str(uuid.uuid4())
    while player_id in players:
        player_id = str(uuid.uuid4())
    return player_id

def nickname_available(nickname):
    for player_id in players:
        if players[player_id]['nickname'] == nickname:
            return False
    return True

def new_player(nickname):
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
    if nickname_available(nickname):
        return new_player(nickname)
    return None

def get_player_by_id(player_id):
    if player_id in players:
        return players[player_id]
    return None

def get_all_players():
    return [x for x in players.values()]

def set_player_team(player_id, team):
    if player_id in players and not players[player_id]['team']:
        players[player_id]['team'] = team
        return True
    return False

def delete_players():
    players.clear()

# ELO rating:
# won = 1, lost = 0; else 0.5
# R1 = ELO1, R2 = ELO2
# E = 1 / (1 + pow(10, (R2-R1)/400))
# Rnew = Rold + K * (S - E)
# K =