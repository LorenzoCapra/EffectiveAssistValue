from nba_api.stats.endpoints import leaguedashplayerstats
from definitions import DATA_DIR 
from pathlib import Path

season = '2022-23'
endpoint_handler = leaguedashplayerstats.LeagueDashPlayerStats(season=season)
player_stats_df = endpoint_handler.get_data_frames()[0]


player_stats_folder = Path(DATA_DIR) / "player_stats"
if not player_stats_folder.exists():
    player_stats_folder.mkdir()

player_stats_df.to_csv(player_stats_folder / f"player_stats_data_season_{season}.csv", index=False)
