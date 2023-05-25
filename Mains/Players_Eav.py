import pandas as pd
import numpy as np

from nba_api.stats.endpoints import leaguedashplayerstats

team_ids = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
            'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
            'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

season = '2022-23'
gp_threshold = 41  # threshold on games played by a player

for abb in team_ids:
    print(f'--------------------------------------------------------')
    print(f'Iterating over {abb}...')
    print(f'--------------------------------------------------------')

    TEAM_NAME = abb
    TEAM = pd.read_csv(f'CSV/SEASON_22_23/{TEAM_NAME}_SEASON_EAV.csv')

    # Check how many games each player has played during the season
    df_league_all = leaguedashplayerstats.LeagueDashPlayerStats(season=season, season_type_all_star='Regular Season')
    df_stats_all = df_league_all.get_data_frames()[0]
    df_gp = df_stats_all.loc[:, ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'MIN', 'AST']]
    # Games played for each Lakers player
    df_lal_gp = df_gp.loc[df_gp['TEAM_ABBREVIATION'] == TEAM_NAME]

    single_player_eav = []
    mean_single_player_eav = []
    players_list = []
    player_gp = []

    for player in TEAM['Player'].unique():
        count = 0
        for p in df_lal_gp['PLAYER_NAME']:
            if p == player:
                player_gp.append(df_lal_gp.iloc[count, 2])
                break
            else:
                count += 1
        for i in range(TEAM.shape[0]):
            if TEAM.iloc[i, 0] == player:
                single_player_eav.append(TEAM.iloc[i, 2])

        diff = player_gp[-1] - len(single_player_eav)
        for k in range(diff):
            single_player_eav.append(0)

        # Check on number of games played
        if player_gp[-1] > gp_threshold:
            players_list.append(player)
            mean_single_player_eav.append(round(np.mean(single_player_eav), 3))

        single_player_eav = []

    # Dictionary of lists
    lal_dict = {'Player': players_list, 'AVG EAV': mean_single_player_eav}
    players_average_eav = pd.DataFrame(lal_dict)

    # print(players_average_eav)

    # Saving the dataframe
    players_average_eav.to_csv(f'CSV/PLAYERS_EAV_22_23/{TEAM_NAME}_PLAYERS_AVG_EAV.csv', header=True, index=False)
