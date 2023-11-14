"""
This file contains some utilities functions.
"""

# Import general dependencies
import matplotlib as mpl
import pandas as pd
import numpy as np
import re

# Import API endpoints used
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import leaguedashteamshotlocations


# Function to draw basketball court
def create_court(ax, color):
    # Short corner 3PT lines
    ax.plot([-220, -220], [0, 140], linewidth=2, color=color)
    ax.plot([220, 220], [0, 140], linewidth=2, color=color)

    # 3PT Arc
    ax.add_artist(mpl.patches.Arc((0, 140), 440, 315, theta1=0, theta2=180, facecolor='none', edgecolor=color, lw=2))

    # Lane and Key
    ax.plot([-80, -80], [0, 190], linewidth=2, color=color)
    ax.plot([80, 80], [0, 190], linewidth=2, color=color)
    ax.plot([-60, -60], [0, 190], linewidth=2, color=color)
    ax.plot([60, 60], [0, 190], linewidth=2, color=color)
    ax.plot([-80, 80], [190, 190], linewidth=2, color=color)
    ax.add_artist(mpl.patches.Circle((0, 190), 60, facecolor='none', edgecolor=color, lw=2))

    # Rim
    ax.add_artist(mpl.patches.Circle((0, 60), 15, facecolor='none', edgecolor=color, lw=2))

    # Backboard
    ax.plot([-30, 30], [40, 40], linewidth=2, color=color)
    # Remove ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # Set axis limits
    ax.set_xlim(-250, 250)
    ax.set_ylim(0, 470)
    # General plot parameters
    mpl.rcParams['font.family'] = 'Avenir'
    mpl.rcParams['font.size'] = 18
    mpl.rcParams['axes.linewidth'] = 2


def games_in_1_season(season, season_type='Regular Season'):
    """
    Function to get all the games with their respective ids for 1 specific season.
    :param season: string
    :param season_type: string
    :return: games -> dataframe, game_ids -> list
    """
    # Get game logs from the specified regular season
    gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season,
                                                   league_id_nullable='00',
                                                   season_type_nullable=season_type)
    games = gamefinder.get_data_frames()[0]

    # Get a list of the distinct game_ids
    game_ids = games['GAME_ID'].unique().tolist()

    return games, game_ids


def players_eav_in_1_game(pbp, i=None, restrict_to_crunch_time:bool=False):
    """
    Function to extract the EAV values of each player for a specific game

    Inputs:
    - DataFrame of the Play-By-Play data for a specific game
    - Index of the game to search for

    Outputs:
    - DataFrame containing each player and their respective EAV for the specific game

    Author: Lorenzo Capra
    """
    if i is not None:
        print(f'... searching for game {i+1} ...')

    # Keep only the useful columns from the PBP dataframe
    pbp_restrict = pbp.loc[:, ['HOMEDESCRIPTION', 'VISITORDESCRIPTION', 'PLAYER1_ID',
                               'PLAYER1_NAME', 'PLAYER2_ID', 'PLAYER2_NAME', 'PLAYER2_TEAM_ABBREVIATION', 'PCTIMESTRING', 'PERIOD']]
    
    if restrict_to_crunch_time:
        pbp_restrict = pbp_restrict[(pbp_restrict['PCTIMESTRING'].apply(lambda x: int("".join(x.split(':')))<=500)) & (pbp_restrict['PERIOD']==4)]
        pbp_restrict = pbp_restrict.loc[:, ['HOMEDESCRIPTION', 'VISITORDESCRIPTION', 'PLAYER1_ID',
                               'PLAYER1_NAME', 'PLAYER2_ID', 'PLAYER2_NAME', 'PLAYER2_TEAM_ABBREVIATION']]

    # Build a PBP dataframe which considers only plays with an assist
    pbp_ast = pd.DataFrame()

    for i in range(pbp_restrict.shape[0]):
        if i == 0:
            i += 1
        else:
            if pbp_restrict.iloc[i][0] != None and 'AST' in pbp_restrict.iloc[i][0]:
                pbp_row = pd.DataFrame([pbp_restrict.iloc[i]])
                pbp_ast = pd.concat([pbp_ast, pbp_row], ignore_index=True)
            elif pbp_restrict.iloc[i][1] != None and 'AST' in pbp_restrict.iloc[i][1]:
                pbp_row = pd.DataFrame([pbp_restrict.iloc[i]])
                pbp_ast = pd.concat([pbp_ast, pbp_row], ignore_index=True)

    # Extract relevant information from the pbp_ast dataframe:
    # -> distance of the made field goal
    numbers1 = np.zeros((pbp_ast.shape[0]))
    for j in range(pbp_ast.shape[0]):
        if pbp_ast.iloc[j][0] is not None:
            num = re.findall(r'\d+', pbp_ast.iloc[j][0])
            num = eval(num[0])
            numbers1[j] = num

    numbers2 = np.zeros((pbp_ast.shape[0]))
    for j in range(pbp_ast.shape[0]):
        if pbp_ast.iloc[j][1] is not None:
            num = re.findall(r'\d+', pbp_ast.iloc[j][1])
            num = eval(num[0])
            numbers2[j] = num

    # Insert these information in the pbp_ast dataframe
    pbp_ast['HOMEDESCRIPTION'] = numbers1
    pbp_ast['VISITORDESCRIPTION'] = numbers2

    # Now we look for league wise shots information, recalling that:
    # Restricted Area -> 0-4 feet
    # Paint (non RA) -> 4-15 feet
    # Mid-Range -> 16-22/23 feet
    # 3 Points -> 22/23-inf feet

    teamshotlocation = leaguedashteamshotlocations.LeagueDashTeamShotLocations(season='2021-22',
                                                                               league_id_nullable='00',
                                                                               season_type_all_star='Regular Season',
                                                                               distance_range='By Zone')
    shotloc = teamshotlocation.get_data_frames()[0]

    shotlocperc = shotloc.loc[:, ['Restricted Area', 'In The Paint (Non-RA)', 'Mid-Range', 'Above the Break 3']]
    shotlocperc = shotlocperc.xs('FG_PCT', axis=1, level=1)

    # Compute average % from each distance range
    meanshotperc = shotlocperc.mean()

    # Calculate the EAV associated to each assist of the specific game
    eav = np.zeros((pbp_ast.shape[0]))

    for i in range(pbp_ast.shape[0]):
        play = pbp_ast.loc[i, ['HOMEDESCRIPTION', 'VISITORDESCRIPTION']]
        hplay = play[0]
        vplay = play[1]

        if hplay != 0.0:
            if 0 < hplay <= 4:
                eav[i] = round(2 * meanshotperc[0], 3)
            elif 4 < hplay <= 15:
                eav[i] = round(2 * meanshotperc[1], 3)
            elif 15 < hplay <= 22:
                eav[i] = round(2 * meanshotperc[2], 3)
            elif 22 < hplay <= 30:
                eav[i] = round(3 * meanshotperc[3], 3)
            else:
                eav[i] = 3 * 0.2
        elif vplay != 0.0:
            if 0 < vplay <= 4:
                eav[i] = round(2 * meanshotperc[0], 3)
            elif 4 < vplay <= 15:
                eav[i] = round(2 * meanshotperc[1], 3)
            elif 15 < vplay <= 22:
                eav[i] = round(2 * meanshotperc[2], 3)
            elif 22 < vplay <= 30:
                eav[i] = round(3 * meanshotperc[3], 3)
            else:
                eav[i] = 3 * 0.2

    # Insert the EAV values in the pbp_ast dataframe
    if pbp_ast.shape[0] != 0:
        pbp_ast.insert(7, 'EAV', eav, True)

        # Assign the values to each player corresponding to the type of assist
        players_eav = np.array(['Player', 'Team', 'EAV'])
        df_plays_eav = pbp_ast.loc[:, ['PLAYER2_NAME', 'PLAYER2_TEAM_ABBREVIATION', 'EAV']]

        for player in pd.unique(pbp_ast.loc[:, 'PLAYER2_NAME']):
            count = 0
            team = None
            for i in range(df_plays_eav.shape[0]):
                if df_plays_eav.iloc[i, 0] == player:
                    count += df_plays_eav.iloc[i, 2]
                    team = df_plays_eav.iloc[i, 1]

            players_eav = np.concatenate((players_eav, np.array([player, team, count])))

        players_eav = players_eav.reshape(len(pd.unique(pbp_ast.loc[:, 'PLAYER2_NAME'])) + 1, 3)

        # Transform into dataframe & return it
        df_players_eav = pd.DataFrame(players_eav[1:, :], columns=['Player', 'Team', 'EAV'])

    else:
        df_players_eav = pd.DataFrame()

    return df_players_eav