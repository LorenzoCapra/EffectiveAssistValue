from nba_api.stats.static import players


class Player:
    def __init__(self, first_name, last_name):

        self.first_name = first_name
        self.last_name = last_name
        self.player_id = -1

        # Load players file
        self.players_dict = players.get_players()

    # Get player ID based on player name
    def get_player_id(self):
        for player in self.players_dict:
            if player['first_name'] == self.first_name and player['last_name'] == self.last_name:
                self.player_id = player['id']
                return self.player_id
        return -1
