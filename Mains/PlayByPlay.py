from nba_api.stats.endpoints import playbyplayv2
from Tools.Utils import players_eav_in_1_game, games_in_1_season


games, game_ids = games_in_1_season(season='2021-22', season_type='Regular Season')

# Get ID of the 100th game
game_id = game_ids[100]

# Get play-by-play data for the 100th game
pbp = playbyplayv2.PlayByPlayV2(game_id)
pbp = pbp.get_data_frames()[0]

'''Compute EAV for each player of this game'''
df_eav = players_eav_in_1_game(pbp)
print(df_eav)
