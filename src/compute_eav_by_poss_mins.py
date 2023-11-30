from pathlib import Path
import pandas as pd
from definitions import DATA_DIR

data_dir_path = Path(DATA_DIR)
player_stats_folder = data_dir_path / "player_stats"
season = '2022-23'
player_avg_eav_df = pd.read_csv(data_dir_path / f"PLAYERS_AVG_EAV.csv")
player_stats_df = pd.read_csv(player_stats_folder / f"player_stats_data_season_{season}.csv")
possessions_df = pd.read_csv(data_dir_path / f"possessions.csv")

merged_df = player_avg_eav_df.merge(possessions_df, left_on='Team', right_on='TEAM', how='left')

player_stats_df_sub = player_stats_df[['PLAYER_NAME', 'MIN', 'GP']]

merged_df2 = player_stats_df_sub.merge(merged_df, left_on='PLAYER_NAME', right_on='Player', how='left')

df_subcolumns = merged_df2[['Player', 'AVG EAV', 'TEAM', ' poss', 'MIN', 'GP']]
df_subcolumns = df_subcolumns.loc[(df_subcolumns['GP'] >= 41)]
df_subcolumns['average_minutes_played_by_each_player'] = df_subcolumns['MIN'] / df_subcolumns['GP']

df_subcolumns['poss_factor'] = df_subcolumns['average_minutes_played_by_each_player'] * df_subcolumns[' poss'] / 48
df_subcolumns['eav_corrected'] = df_subcolumns['AVG EAV'] / df_subcolumns['poss_factor']

df_subcolumns.to_csv(player_stats_folder / "player_average_eav_by_possessions.csv")

df_ranking = df_subcolumns.sort_values(by=['eav_corrected'], axis=0, ascending=False).reset_index(drop=True)

print(df_ranking.head(10))