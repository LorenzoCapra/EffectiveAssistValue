from pathlib import Path
import pandas as pd
from definitions import DATA_DIR

data_dir_path = Path(DATA_DIR)
player_stats_folder = data_dir_path / "player_stats"
season = '2022-23'
player_avg_eav_df = pd.read_csv(data_dir_path / f"PLAYERS_AVG_EAV.csv")
player_stats_df = pd.read_csv(player_stats_folder / f"player_stats_data_season_{season}.csv")

player_stats_df_sub = player_stats_df[['PLAYER_NAME', 'AST', 'GP']]
player_stats_df_sub['AVG AST'] = player_stats_df_sub['AST'] / player_stats_df_sub['GP']

merged_df = player_avg_eav_df.merge(player_stats_df_sub[['PLAYER_NAME', 'AVG AST']], left_on='Player', right_on='PLAYER_NAME', how='left')

df_subcolumns = merged_df[['Player', 'Team', 'AVG EAV', 'AVG AST']]

df_subcolumns.to_csv(player_stats_folder / "players_eav_vs_ast_by.csv")

df_ranking_eav = df_subcolumns.sort_values(by=['AVG EAV'], axis=0, ascending=False).reset_index(drop=True)
df_ranking_ast = df_subcolumns.sort_values(by=['AVG AST'], axis=0, ascending=False).reset_index(drop=True)

df_subcolumns['DIFF'] = df_subcolumns['AVG EAV'] - df_subcolumns['AVG AST']
df_subcolumns.to_csv(player_stats_folder / "players_eav_vs_ast_by.csv")

df_ranking_diff = df_subcolumns.sort_values(by=['DIFF'], axis=0, ascending=False).reset_index(drop=True)

print(df_ranking_diff.head(10))