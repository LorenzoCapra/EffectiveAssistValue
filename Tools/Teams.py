from nba_api.stats.static import teams


class Team:
    def __init__(self, team_name):

        self.team_name = team_name
        self.team_id = -1

        # Load teams file
        self.teams = teams.get_teams()

    # Get team ID based on team name
    def get_team_id(self):
        for team in self.teams:
            if team['full_name'] == self.team_name:
                self.team_id = team['id']
                return self.team_id
        return -1
