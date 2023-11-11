# Import packages
from nba_api.stats.endpoints import shotchartdetail

from tools.Teams import Team
from tools.Players import Player
from tools.utils import create_court

import json
import pandas as pd
import matplotlib.pyplot as plt

LAL = Team("Los Angeles Lakers")
LBJ = Player("LeBron", "James")

print(LAL.get_team_id())
print(LBJ.get_player_id())

# Create JSON request
shot_json = shotchartdetail.ShotChartDetail(
            team_id=LAL.get_team_id(),
            player_id=LBJ.get_player_id(),
            context_measure_simple='PTS',
            season_nullable='2022-23',
            season_type_all_star='Regular Season')

# Load data into a Python dictionary
shot_data = json.loads(shot_json.get_json())

# Get the relevant data from our dictionary
relevant_data = shot_data['resultSets'][0]

# Get the headers and row data
headers = relevant_data['headers']
rows = relevant_data['rowSet']

# Create pandas DataFrame
lebron_data = pd.DataFrame(rows)
lebron_data.columns = headers

# Draw basketball court
fig = plt.figure(figsize=(4, 3.76))
ax = fig.add_axes([0, 0, 1, 1])
create_court(ax, 'black')

# Plot hexbin of shots
ax.hexbin(lebron_data['LOC_X'], lebron_data['LOC_Y'] + 60, gridsize=(30, 30),
          extent=(-300, 300, 0, 940), bins='log', cmap='Blues')

plt.show()
