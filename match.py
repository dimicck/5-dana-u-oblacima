import math

from team import get_team_by_id, average_team_elo

matches = {}

def validate_teams(team1Id, team2Id, winningTeamId):
    if team1Id == team2Id or not get_team_by_id(team1Id) or not get_team_by_id(team2Id):
        return False
    if winningTeamId and (winningTeamId != team1Id and winningTeamId != team2Id):
        return False
    return True

def get_expected_elo(r1, r2):
    return 1 / (1 + math.pow(10, (r2 - r1) / 400))

def get_rating_adjustment(hours):
    if hours < 500: return 50
    if hours < 1000: return 40
    if hours < 3000: return 30
    if hours < 5000: return 20
    return 10

def update_elo(player, r2, s):
    r1 = player['elo']
    e = get_expected_elo(r1, r2)
    k = get_rating_adjustment(player['hoursPlayed'])
    player['elo'] = r1 + k*(s - e)

def update_team_stats(team, r2, s, duration):
    # s == 0   : lost
    # s == 1   : won
    # else s == 0.5
    team = get_team_by_id(team)
    for player in team['players']:
        player['hoursPlayed'] += duration
        if not s:
            player['losses'] += 1
        elif s == 1:
            player['wins'] += 1
        
        update_elo(player, r2, s)

def is_winner_team(teamId, winningTeamId):
    if not winningTeamId:
        return 0.5
    return teamId == winningTeamId

def add_new_match(team1Id, team2Id, winningTeamId, duration):
    if validate_teams(team1Id, team2Id, winningTeamId) and duration >= 1:
        team1_elo = average_team_elo(team1Id)
        team2_elo = average_team_elo(team2Id)
        update_team_stats(team1Id, team2_elo, is_winner_team(team1Id, winningTeamId), duration)
        update_team_stats(team2Id, team1_elo, is_winner_team(team2Id, winningTeamId), duration)
        return True

    return False

