import pandas as pd
import time

from nba_api.stats.endpoints import playbyplayv2
from Tools.Utils import players_eav_in_1_game, games_in_1_season


games, game_ids = games_in_1_season(season='2022-23', season_type='Regular Season')

# Get ID of the 100th game
game_id = game_ids[100]

# Get play-by-play data for the 100th game
pbp = playbyplayv2.PlayByPlayV2(game_id)
pbp = pbp.get_data_frames()[0]

'''Compute EAV for each player of this game'''
# df_eav = players_eav_in_1_game(pbp)


'''Search for all LAL games'''
games_restrict = games.loc[:, ['TEAM_ABBREVIATION', 'GAME_ID']]

team_ids = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
            'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
            'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

for abb in team_ids:
    print(f'--------------------------------------------------------')
    print(f'Iterating over {abb}...')
    print(f'--------------------------------------------------------')

    TEAM_NAME = abb
    _games_id = []

    for i in range(games_restrict.shape[0]):
      team = TEAM_NAME
      if games_restrict.iloc[i, 0] == team:
        _games_id.append(games_restrict.iloc[i, 1])

    df_players_eav = pd.DataFrame()
    for j in range(len(_games_id)):
      game_id = _games_id[j]

      time.sleep(0.2)

      pbp_ = playbyplayv2.PlayByPlayV2(game_id)
      pbp_ = pbp_.get_data_frames()[0]

      time.sleep(0.5)

      eav_game = players_eav_in_1_game(pbp_, j)

      df_players_eav = pd.concat([df_players_eav, eav_game], ignore_index=True)

    LAL = pd.DataFrame()

    for k in range(df_players_eav.shape[0]):
      if df_players_eav.iloc[k, 1] == TEAM_NAME:
        LAL = pd.concat([LAL, df_players_eav.iloc[k, :]], axis=1, ignore_index=True)

    LAL = LAL.transpose()

    # Saving the dataframe
    LAL.to_csv(f'CSV/SEASON_22_23/{TEAM_NAME}_SEASON_EAV.csv', header=True, index=False)
