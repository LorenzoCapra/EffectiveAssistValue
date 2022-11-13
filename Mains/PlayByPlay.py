import pandas as pd
import time

from nba_api.stats.endpoints import playbyplayv2
from Tools.Utils import players_eav_in_1_game, games_in_1_season


games, game_ids = games_in_1_season(season='2021-22', season_type='Regular Season')

# Get ID of the 100th game
game_id = game_ids[100]

# Get play-by-play data for the 100th game
pbp = playbyplayv2.PlayByPlayV2(game_id)
pbp = pbp.get_data_frames()[0]

'''Compute EAV for each player of this game'''
# df_eav = players_eav_in_1_game(pbp)


'''Search for all LAL games'''
games_restrict = games.loc[:, ['TEAM_ABBREVIATION', 'GAME_ID']]

lal_games_id = []

for i in range(games_restrict.shape[0]):
  team = 'LAL'
  if games_restrict.iloc[i, 0] == team:
    lal_games_id.append(games_restrict.iloc[i, 1])

df_players_eav = pd.DataFrame()
for i in range(len(lal_games_id)):
  game_id = lal_games_id[i]

  time.sleep(0.5)

  pbp_ = playbyplayv2.PlayByPlayV2(game_id)
  pbp_ = pbp_.get_data_frames()[0]

  time.sleep(0.5)

  eav_game = players_eav_in_1_game(pbp_, i)

  df_players_eav = pd.concat([df_players_eav, eav_game], ignore_index=True)

# Saving the dataframe
df_players_eav.to_csv('LAL_SEASON_EAV.csv', header=True, index=False)
