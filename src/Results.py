"""
File to return some results (hopefully)
"""

# Import general dependencies
import pandas as pd

# Define all the possible team ids to iterate on
team_ids = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
            'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
            'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

playoff_team_ids = ['ATL', 'BKN', 'BOS', 'CLE', 'DEN', 'GSW', 'LAC', 'LAL',
                    'MEM', 'MIA', 'MIL', 'MIN', 'NYK', 'PHI', 'PHX', 'SAC']

season = '2022-23'

# Create a dataframe containing all the players with their average EAV
all_players_eav = pd.DataFrame()

for abb in playoff_team_ids:
    TEAM_NAME = abb
    TEAM = pd.read_csv(f'../data/PLAYERS_{season}_playoffs/{TEAM_NAME}_PLAYERS_AVG_EAV_playoffs.csv')

    all_players_eav = pd.concat([all_players_eav, TEAM], axis=0, ignore_index=True)

# Sort the players by average EAV to rank them
all_players_eav = all_players_eav.sort_values(by=['AVG EAV'], axis=0, ascending=False).reset_index(drop=True)

# Print TOP 10
print(all_players_eav.head(10))