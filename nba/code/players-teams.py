#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 20:46:29 2019

@author: tkh5044
"""

import pandas as pd

# Get static data - NBA players and teams
from nba_api.stats.static import teams, players
from nba_api.stats.endpoints import *

# players
def get_nba_players():
    nba_players = pd.DataFrame(players.get_players())
    nba_players = nba_players[['id', 'full_name', 'first_name', 'last_name', 'is_active']]
    print(f'Number of players fetched: {len(nba_players)}')
    nba_players.to_csv('../data/nba_players.csv', index=False)

    # active
    active = nba_players[nba_players.is_active]
    print(f'Number of active players: {len(active)}')
    active.to_csv('../data/nba_players_active.csv', index=False)

    # inactive
    inactive = nba_players[~nba_players.is_active]
    print(f'Number of active players: {len(inactive)}')
    inactive.to_csv('../data/nba_players_inactive.csv', index=False)


# teams
def get_nba_teams():
    nba_teams = pd.DataFrame(teams.get_teams())
    nba_teams[['id', 'full_name', 'abbreviation', 'nickname', 'city', 'state', 'year_founded']]
    print(f'Number of teams fetched: {len(nba_teams)}')
    nba_teams.to_csv('../data/nba_teams.csv', index=False)


# player career stats
def get_player_career_stats():
    nba_players = pd.DataFrame(players.get_players())
    player_ids = nba_players.id.tolist()
    career = pd.DataFrame()
    for pid in player_ids:
        df = playercareerstats.PlayerCareerStats(player_id=pid).get_data_frames()[0]
        career = career.append(df, ignore_index=True)
    
    # map player ID to player name
    cols = career.columns.tolist()
    cols.insert(1, 'PLAYER_NAME')
    player_id_map = nba_players[['id', 'full_name']].set_index('id')
    career['PLAYER_NAME'] = career.PLAYER_ID.map(player_id_map.full_name)
    career = career[cols]
    
    # output with single season team splits
    career.to_csv('../data/player_career_stats_w_team_splits.csv', index=False)
    
    # filter to only aggregated/full seasons
    playerlist = (career.PLAYER_ID.astype(str) + career.SEASON_ID).tolist()
    c = [playerlist.count(i) for i in playerlist]
    wo_team_splits = career[(pd.Series(c) == 1) | (career.TEAM_ABBREVIATION == 'TOT')]
    wo_team_splits.to_csv('../data/player_season_stats.csv', index=False)
    