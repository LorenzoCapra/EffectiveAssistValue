"""
This is the main file, from which the pipeline starts. The script runs nested for loops over
all the NBA teams first and then over all the games played by each team.
Then another loop on each play of each single game is run, to retrieve all the assists.
The EAV formula is then applied to transform each assist to its corresponding EAV value, and
it is associated to the specific player that make the assist.
At the end of the script the .csv files containing all the EAVs computed for each assist
made by the players of each team are stored in the CSV folder.
"""

# Import general dependencies
import pandas as pd
import time
import os

# Import API endpoints used
from nba_api.stats.endpoints import playbyplayv2

# Import functionalities from other files
from Tools.Utils import players_eav_in_1_game, games_in_1_season

# Get the all the games played in 1 NBA season with their respective ids
season = '2022-23'
games, game_ids = games_in_1_season(season=season, season_type='Regular Season')

# Shrink the games dataframe to contain only necessary information: team and game id
games_restrict = games.loc[:, ['TEAM_ABBREVIATION', 'GAME_ID']]

# Define all the possible team ids to iterate on
team_ids = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
            'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
            'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

# Perform the loop checking on all teams name abbreviations
for abb in team_ids:
    print(f'--------------------------------------------------------')
    print(f'Iterating over {abb}...')
    print(f'--------------------------------------------------------')

    TEAM_NAME = abb
    _games_id = []

    # Loop over all the games to separate the games played by abb
    for i in range(games_restrict.shape[0]):
      # team = TEAM_NAME
      if games_restrict.iloc[i, 0] == TEAM_NAME:
        _games_id.append(games_restrict.iloc[i, 1])

    df_abb_players_eav = pd.DataFrame()
    # Loop over the games played by abb to get all the plays ending with
    # an assist and computing the corresponding EAV value
    for j in range(len(_games_id)):
      game_id = _games_id[j]

      # Usefull when quering the API
      time.sleep(0.2)

      # Get the playbyplay dataframe from the specified game id
      pbp_ = playbyplayv2.PlayByPlayV2(game_id)
      pbp_ = pbp_.get_data_frames()[0]

      # Usefull when quering the API
      time.sleep(0.5)

      # Compute the EAV for each assist in the specified game
      eav_game = players_eav_in_1_game(pbp_, j)

      # Build the dataframe with all the EAVs for all the assists for every game
      # (this contains both the players of team abb and the players against abb in the specified game)
      df_abb_players_eav = pd.concat([df_abb_players_eav, eav_game], ignore_index=True)

    # Build a new dataframe that selects only the players from team abb
    ABB = pd.DataFrame()

    for k in range(df_abb_players_eav.shape[0]):
      if df_abb_players_eav.iloc[k, 1] == TEAM_NAME:
        ABB = pd.concat([ABB, df_abb_players_eav.iloc[k, :]], axis=1, ignore_index=True)

    ABB = ABB.transpose()

    # Saving the dataframe in the CSV folder
    if not os.path.exists(f'CSV/SEASON_{season}'):
        os.mkdir(f'CSV/SEASON_{season}')
    ABB.to_csv(f'CSV/SEASON_{season}/{TEAM_NAME}_{season}_EAV.csv', header=True, index=False)
