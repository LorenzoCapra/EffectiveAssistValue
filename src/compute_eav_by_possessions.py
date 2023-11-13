from pathlib import Path
import pandas as pd
from definitions import DATA_DIR

data_dir_path = Path(DATA_DIR)
player_stats_folder = data_dir_path / "player_stats"
season = '2022-23'
player_avg_eav_df = pd.read_csv(data_dir_path / f"PLAYERS_AVG_EAV.csv")
possessions_df = pd.read_csv(data_dir_path / f"possessions.csv")

merged_df = player_avg_eav_df.merge(possessions_df, left_on='Team', right_on='TEAM', how='left')

df_subcolumns = merged_df[['Player', 'AVG EAV', 'TEAM', ' poss']]

df_subcolumns['poss_factor'] = 100 / df_subcolumns[' poss']
df_subcolumns['eav_corrected'] = df_subcolumns['AVG EAV'] * df_subcolumns['poss_factor']

df_subcolumns.to_csv(player_stats_folder / "player_average_eav_by_100_possessions.csv")

df_ranking = df_subcolumns.sort_values(by=['eav_corrected'], axis=0, ascending=False).reset_index(drop=True)

print(df_ranking.head(10))