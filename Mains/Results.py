import pandas as pd

team_ids = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW',
            'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK',
            'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

all_players_eav = pd.DataFrame()

for abb in team_ids:
    TEAM_NAME = abb
    TEAM = pd.read_csv(f'CSV/PLAYERS_EAV/{TEAM_NAME}_PLAYERS_AVG_EAV.csv')

    all_players_eav = pd.concat([all_players_eav, TEAM], axis=0, ignore_index=True)

all_players_eav = all_players_eav.sort_values(by=['AVG EAV'], axis=0, ascending=False).reset_index(drop=True)
print(all_players_eav.head(10))