import math

from team import get_team_by_id, average_team_elo

def validate_teams(team1_id, team2_id, winning_team_id):
    """
       Validates the teams IDs

       :param str team1_id: The ID of the first team.
       :param str team2_id: The ID of the second team.
       :param str winning_team_id: The ID of the winning team (optional).

       :return: True if the teams and winning team are valid; False otherwise.
       :rtype: bool
    """
    if team1_id == team2_id or not get_team_by_id(team1_id) or not get_team_by_id(team2_id):
        return False
    if winning_team_id and (winning_team_id != team1_id and winning_team_id != team2_id):
        return False
    return True

def get_expected_elo(r1, r2):
    """
        Calculate the expected ELO rating

        :param float r1: The ELO rating of the player.
        :param float r2: The ELO rating of the opponent team.

        :return: Expected ELO rating
        :rtype: double
    """
    return 1 / (1 + math.pow(10, (r2 - r1) / 400))

def get_rating_adjustment(hours):
    """
        Calculate rating adjustment (K-factor) for player
        The K-factor decreases as the player gains experience.

        :param int hours: The number of hours the player has played.

        :return: Rating adjustment
        :rtype: int
    """
    if hours < 500: return 50
    if hours < 1000: return 40
    if hours < 3000: return 30
    if hours < 5000: return 20
    return 10

def update_elo(player, r2, s):
    """
    Updates the ELO rating of a player based on the match result.

    :param dict player: The player's data
    :param float r2: The average ELO rating of the opposing team.
    :param float s: The score of the match (1 for win, 0 for loss, 0.5 for draw).

    :return: None
    """
    r1 = player['elo']
    e = get_expected_elo(r1, r2)
    k = get_rating_adjustment(player['hoursPlayed'])
    player['ratingAdjustment'] = k
    player['elo'] = r1 + k * (s - e)

def update_team_stats(team, r2, s, duration):
    """
       Updates the stats of all players on a team after a match.

       :param str team: The UUID of the team.
       :param float r2: The average ELO rating of the opposing team.
       :param float s: The score of the match for the team (1 for win, 0 for loss, 0.5 for draw).
       :param int duration: The duration of the match in hours.

       :return: None
       """
    team = get_team_by_id(team)
    for player in team['players']:
        player['hoursPlayed'] += duration
        if not s:
            player['losses'] += 1
        elif s == 1:
            player['wins'] += 1
        
        update_elo(player, r2, s)

def is_winner_team(team_id, winning_team_id):
    """
       Determines match status for the given team.

       :param str team_id: The UUID of the team.
       :param str winning_team_id: The ID of the winning team.

       :return: 1 if the team won, 0 if it lost, and 0.5 for a draw.
       :rtype: float
    """
    if not winning_team_id:
        return 0.5
    return team_id == winning_team_id

def add_new_match(team1_id, team2_id, winning_team_id, duration):
    """
       Records a new match between two teams.

       Updates team and player stats, including wins, losses, hours played, and ELO ratings.

       :param str team1_id: The UUID of the first team.
       :param str team2_id: The UUID of the second team.
       :param str winning_team_id: The UUID of the winning team (optional).
       :param int duration: The duration of the match in hours.

       :return: True if the match was successfully added, False otherwise.
       :rtype: bool
       """
    if validate_teams(team1_id, team2_id, winning_team_id) and duration >= 1:
        team1_elo = average_team_elo(team1_id)
        team2_elo = average_team_elo(team2_id)
        update_team_stats(team1_id, team2_elo, is_winner_team(team1_id, winning_team_id), duration)
        update_team_stats(team2_id, team1_elo, is_winner_team(team2_id, winning_team_id), duration)
        return True

    return False

