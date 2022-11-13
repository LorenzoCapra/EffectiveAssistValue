import pandas as pd
import numpy as np

from nba_api.stats.endpoints import leaguedashplayerstats

lal_eav = pd.read_csv('LAL_SEASON_EAV.csv')
df_lal_eav = pd.DataFrame(lal_eav)
# print(df_lal_eav.head())

LAL = pd.DataFrame()

for i in range(df_lal_eav.shape[0]):
  if df_lal_eav.iloc[i, 1] == 'LAL':
    LAL = pd.concat([LAL, df_lal_eav.iloc[i, :]], axis=1, ignore_index=True)

LAL = LAL.transpose()

# print(LAL.head())

# Check how many games each player has played during the season
df_league_all = leaguedashplayerstats.LeagueDashPlayerStats(season='2021-22', season_type_all_star='Regular Season')
df_stats_all = df_league_all.get_data_frames()[0]
df_gp = df_stats_all.loc[:, ['PLAYER_NAME', 'TEAM_ABBREVIATION', 'GP', 'MIN', 'AST']]
# Games played for each Lakers player
df_lal_gp = df_gp.loc[df_gp['TEAM_ABBREVIATION'] == 'LAL']

single_player_eav = []
mean_single_player_eav = []
players_list = []
player_gp = []

for player in LAL['Player'].unique():
    count = 0
    for p in df_lal_gp['PLAYER_NAME']:
        if p == player:
            player_gp.append(df_lal_gp.iloc[count, 2])
            break
        else:
            count += 1
    for i in range(LAL.shape[0]):
        if LAL.iloc[i, 0] == player:
            single_player_eav.append(LAL.iloc[i, 2])

    diff = player_gp[-1] - len(single_player_eav)
    for k in range(diff):
        single_player_eav.append(0)
    mean_single_player_eav.append(round(np.mean(single_player_eav), 3))
    players_list.append(player)

    single_player_eav = []

# Dictionary of lists
lal_dict = {'Player': players_list, 'AVG EAV': mean_single_player_eav}
players_average_eav = pd.DataFrame(lal_dict)

print(players_average_eav)

# Saving the dataframe
players_average_eav.to_csv('LAL_PLAYERS_AVG_EAV.csv', header=True, index=False)
