import unittest
from match import add_new_match
from players import delete_players, create_new_player, get_player_by_id
from team import delete_teams, new_team, TEAM_SIZE, get_team_by_id


def generate_player_ids(start=1,size=TEAM_SIZE):
    player_ids = []
    for i in range(start, size + start):
        player_ids.append(create_new_player(f"Player{i}")['id'])
    return player_ids

class TestPlayer(unittest.TestCase):

    def setUp(self):
        delete_players()

    def test_add_player_successfull(self):
        player = create_new_player("testplayer")
        self.assertIsNotNone(player, "Player should be created successfully")
        self.assertEqual(player['nickname'], "testplayer", "Nickname matches the input")

    def test_add_player_fail(self):
        create_new_player("testplayer")
        player = create_new_player("testplayer")
        self.assertIsNone(player, "Player creation fails if nickname is already used")

    def test_get_player(self):
        player_id = '1'
        player = get_player_by_id(player_id)
        self.assertIsNone(player, "Returns None if id not found")
        player_id = (create_new_player("testplayer"))['id']
        player = get_player_by_id(player_id)
        self.assertIsNotNone(player, "Player should be found successfully")
        self.assertEqual(player_id, player['id'])

class TestTeam(unittest.TestCase):

    def setUp(self):
        delete_teams()
        delete_players()

    def test_team_creation_successfull(self):
        player_ids = generate_player_ids()
        # Create a team
        team_name = "myTeam"
        team = new_team(team_name, player_ids)

        # Assert that the team was created and check the returned team
        self.assertIsNotNone(team)
        self.assertEqual(team['teamName'], team_name)
        self.assertEqual(len(team['players']), TEAM_SIZE)

    def test_teamname_taken(self):
        team1_players = generate_player_ids()
        test_name = "myTeam"
        new_team(test_name, team1_players)

        team2_players = generate_player_ids(start=TEAM_SIZE+1)
        team = new_team(test_name, team2_players)

        self.assertIsNone(team, "Team creation fails if team name is already used")

    def test_team_with_invalid_players_number(self):
        player_ids = generate_player_ids(size=TEAM_SIZE-1)
        team = new_team("failedTeam", player_ids)
        self.assertIsNone(team, "Team must have 5 players")

    def test_player_in_other_team(self):
        player_ids = generate_player_ids()
        new_team("team1", player_ids)
        team = new_team("team2", player_ids)

        self.assertIsNone(team, "Team creation fails if player already in other team")

    def test_get_team_by_id(self):
        player_ids = generate_player_ids()
        team = new_team("team", player_ids)
        result = get_team_by_id(team['id'])

        self.assertIsNotNone(result)
        self.assertEqual(result, team)
        # compares keys and values for dictionaries

    def test_get_team_by_id_fail(self):
        team = get_team_by_id("random_id")
        self.assertIsNone(team)

class TestMatch(unittest.TestCase):

    def setUp(self):
        delete_players()
        delete_teams()
        self.team1 = new_team("team1", generate_player_ids())
        self.team2 = new_team("team2", generate_player_ids(start=TEAM_SIZE + 1))

    def test_valid_match(self):
        result = add_new_match(self.team1['id'], self.team2['id'], self.team1['id'], 120)
        self.assertTrue(result)

        stats1 = get_team_by_id(self.team1['id'])
        stats2 = get_team_by_id(self.team2['id'])

        # Check player stats
        for player in stats1['players']:
            self.assertEqual(player['wins'], 1)
            self.assertEqual(player['losses'], 0)
            self.assertEqual(player['hoursPlayed'], 120)

        for player in stats2['players']:
            self.assertEqual(player['wins'], 0)
            self.assertEqual(player['losses'], 1)
            self.assertEqual(player['hoursPlayed'], 120)

    def test_no_winner(self):

        result = add_new_match(self.team1['id'], self.team2['id'], None, 120)
        self.assertTrue(result)

        stats1 = get_team_by_id(self.team1['id'])
        stats2 = get_team_by_id(self.team2['id'])

        # Check player stats
        for player in stats1['players']:
            self.assertEqual(player['wins'], 0)
            self.assertEqual(player['losses'], 0)
            self.assertEqual(player['hoursPlayed'], 120)

        for player in stats2['players']:
            self.assertEqual(player['wins'], 0)
            self.assertEqual(player['losses'], 0)
            self.assertEqual(player['hoursPlayed'], 120)

    def test_same_teams_in_match(self):
        result = add_new_match(self.team1['id'], self.team1['id'], self.team1['id'], 120)
        self.assertFalse(result)

    def test_team_non_existing(self):
        result = add_new_match("random_id", self.team2['id'], None, 120)
        self.assertFalse(result)

    def test_duration_not_valid(self):
        result = add_new_match(self.team1['id'], self.team2['id'], self.team1['id'], 0)
        self.assertFalse(result, "Duration should not be less than 1")