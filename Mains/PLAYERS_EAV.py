"""
This file is to be run after TEAM_EAV. It perform a loop over each team to compute the
average EAV for each player over 1 season. A filter on the data is applied to avoid
considering players that may have played very few games: the threshold is set
to half season, so 41 games.
At the end a .csv file containing the average EAV of each player is saved.
"""

# Import general dependencies
import pandas as pd
import numpy as np
import os

# Import API endpoints used
from nba_api.stats.endpoints import leaguedashplayerstats

# Define all the possible team ids to iterate on
team_ids = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
            'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
            'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

# Specify the season and the games played threshold
season = '2022-23'
gp_threshold = 41  # threshold on games played by a player

# Iterate over every team abbreviation
for abb in team_ids:
    print(f'--------------------------------------------------------')
    print(f'Iterating over {abb}...')
    print(f'--------------------------------------------------------')

    TEAM_NAME = abb
    # Get the dataframe with the EAV associated to all the assists made
    # by the players of team abb during the season
    TEAM = pd.read_csv(f'CSV/SEASON_22_23/{TEAM_NAME}_SEASON_EAV.csv')

    # Check how many games each player has played during the season
    df_league_all = leaguedashplayerstats.LeagueDashPlayerStats(season=season, season_type_all_star='Regular Season')
    df_stats_all = df_league_all.get_data_frames()[0]
    # Shrink the dataset to the necessary information
    df_gp = df_stats_all.loc[:, ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'MIN', 'AST']]
    # Games played for each player of abb team
    df_abb_gp = df_gp.loc[df_gp['TEAM_ABBREVIATION'] == TEAM_NAME]

    # Instantiate lists
    single_player_eav = []
    mean_single_player_eav = []
    players_list = []
    player_gp = []

    # Loop over the players in the abb team
    for player in TEAM['Player'].unique():
        count = 0
        for p in df_abb_gp['PLAYER_NAME']:
            if p == player:
                player_gp.append(df_abb_gp.iloc[count, 2])
                break
            else:
                count += 1
        for i in range(TEAM.shape[0]):
            if TEAM.iloc[i, 0] == player:
                single_player_eav.append(TEAM.iloc[i, 2])

        # Append zeros for the games in which the player looped on has not played
        diff = player_gp[-1] - len(single_player_eav)
        for k in range(diff):
            single_player_eav.append(0)

        # Check on number of games played
        if player_gp[-1] > gp_threshold:
            players_list.append(player)
            mean_single_player_eav.append(round(np.mean(single_player_eav), 3))

        single_player_eav = []

    # Dictionary of lists to create the dataframe
    abb_dict = {'Player': players_list, 'AVG EAV': mean_single_player_eav}
    players_average_eav = pd.DataFrame(abb_dict)

    # Saving the dataframe in the CSV folder
    if not os.path.exists(f'CSV/PLAYERS_{season}'):
        os.mkdir(f'CSV/PLAYERS_{season}')
    players_average_eav.to_csv(f'CSV/PLAYERS_{season}/{TEAM_NAME}_PLAYERS_AVG_EAV.csv', header=True, index=False)
