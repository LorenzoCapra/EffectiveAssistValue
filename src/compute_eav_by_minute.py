from pathlib import Path
import pandas as pd 
from definitions import DATA_DIR

data_dir_path = Path(DATA_DIR)
player_stats_folder = data_dir_path / "player_stats"
season = '2022-23'
player_stats_df = pd.read_csv(player_stats_folder / f"player_stats_data_season_{season}.csv")
player_eav_folder = data_dir_path / "PLAYERS_2022-23"

read_df_list = []
for filepath in player_eav_folder.glob("*.csv"):
    tmp_df = pd.read_csv(filepath)
    read_df_list.append(tmp_df)

all_eavs_df = pd.concat(read_df_list, axis=0)

print("all_eavs_df.shape", all_eavs_df.shape)
print("player_stats_df.shape", player_stats_df.shape)

merged_df = player_stats_df.merge(all_eavs_df, left_on='PLAYER_NAME', right_on='Player', how='left')

df_subcolumns = merged_df[['PLAYER_ID','Player', 'AVG EAV', 'MIN']]
number_of_matches = 82
df_subcolumns['average_minutes_played_by_each_player'] = df_subcolumns['MIN'] / number_of_matches
df_subcolumns['minutes_factor'] = 36 / df_subcolumns['average_minutes_played_by_each_player'] 
df_subcolumns['eav_corrected'] = df_subcolumns['AVG EAV'] * df_subcolumns['minutes_factor'] 

df_subcolumns.to_csv(player_stats_folder / "player_average_eav_by_36_minutes.csv")