import pandas as pd
import numpy as np

lal_eav = pd.read_csv('LAL_SEASON_EAV.csv')
df_lal_eav = pd.DataFrame(lal_eav)
# print(df_lal_eav.head())

LAL = pd.DataFrame()

for i in range(df_lal_eav.shape[0]):
  if df_lal_eav.iloc[i, 1] == 'LAL':
    LAL = pd.concat([LAL, df_lal_eav.iloc[i, :]], axis=1, ignore_index=True)

LAL = LAL.transpose()

# print(LAL.head())

single_player_eav = []
mean_single_player_eav = []
players_list = []

for player in LAL['Player'].unique():
    for i in range(LAL.shape[0]):
        if LAL.iloc[i, 0] == player:
            single_player_eav.append(LAL.iloc[i, 2])

    mean_single_player_eav.append(round(np.mean(single_player_eav), 3))
    players_list.append(player)

    single_player_eav = []

# Dictionary of lists
dict = {'Player': players_list, 'AVG EAV': mean_single_player_eav}
players_average_eav = pd.DataFrame(dict)

print(players_average_eav)

# Saving the dataframe
players_average_eav.to_csv('LAL_PLAYERS_AVG_EAV.csv', header=True, index=False)
