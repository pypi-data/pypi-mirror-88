import requests
import pandas as pd
import datetime
import re
import os
import numpy as np
import matplotlib.pyplot as plt
import unidecode
from sklearn.preprocessing import StandardScaler
from math import pi
from fpl_analytics.FPLUnderStats import GetStats

class FPLAnalytics:
    log_dir = 'logs'
    url_static = "https://fantasy.premierleague.com/api/bootstrap-static/"
    url_fixture_stats = "https://fantasy.premierleague.com/api/fixtures/?event="
    url_player_details = "https://fantasy.premierleague.com/api/element-summary/"
    url_my_team = "https://fantasy.premierleague.com/api/my-team/{0}/" #971608
    
    def __init__(self, save = False):
        
        self.currentGw = self.getCurerntGameWeek()
        self.log_dir = self.log_dir + '/' + str(self.currentGw)
        self.save = save
        
    def getCurerntGameWeek(self):
        raw_data = self.getStaticRawData()
        gameweekInfo = pd.DataFrame(raw_data['events'])
        gameweekInfo = gameweekInfo[gameweekInfo['is_current'] == True]
        return gameweekInfo.id.max() if not np.isnan(gameweekInfo.id.max()) else 0
        
    def saveLog(self, df, fileName):
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
        
        df.to_excel(self.log_dir + '/' + fileName + '.xlsx')
    
    def getStaticRawData(self):
        raw_data = requests.get(self.url_static).json()
        return raw_data
    
    def getTeamDetails(self):
        raw_data = self.getStaticRawData()
            
        teamCols = [
        'id', 'name', 'short_name', 'strength', 'strength_overall_home', 'strength_overall_away',
        'strength_attack_home', 'strength_attack_away', 'strength_defence_home',
        'strength_defence_away']
        teams = pd.DataFrame(raw_data['teams'])
        
        if (self.save):
            self.saveLog(teams, 'team_details')
            
        teams = teams[teamCols]
        teams = teams.sort_values(by = ['strength_overall_home', 'strength_overall_away'], ascending=False)
        return teams
    
    def getGameWeekInfo(self):
        raw_data = self.getStaticRawData()
        gameweekInfo = pd.DataFrame(raw_data['events'])
        
        if (self.save):
            self.saveLog(gameweekInfo, 'gameweek_info')
            
        gameweekInfo = gameweekInfo[[
            'id', 'name', 'deadline_time','average_entry_score', 'finished',
               'highest_score', 'most_selected',
               'most_transferred_in', 'top_element',
               'most_captained', 'most_vice_captained'
        ]]
        return gameweekInfo
    
    def getEventFDR(self,eventId):
        
        event_data = self.getEventDetails(eventId)

        teams = self.getLatestRatings(eventId)
        gameweekInfo = self.getGameWeekInfo()
        
        cols = [
            'event', 
            'deadline_time',
            'team_a_name', 
            'team_h_name', 
            'team_a_difficulty', 
            'team_a_difficulty_attack',
            'team_a_difficulty_defence',
            'team_h_difficulty',
            'team_h_difficulty_attack',
            'team_h_difficulty_defence'
        ]

        # AWAY Stats
        event_data = pd.merge(event_data, teams, how = 'left', left_on='team_a', right_on='id')
        #event_data = event_data[cols + ['name', 'strength_overall_away', 'strength_attack_away', 'strength_defence_away']]
        event_data.rename(columns={'short_name': 'team_a_name', 
                                   'strength_overall_away':'team_a_strength_overall',
                                   'strength_attack_away':'team_a_strength_attack',
                                   'strength_defence_away':'team_a_strength_defence'
                                  }, inplace=True)

        # HOME Stats
        event_data = pd.merge(event_data, teams, how = 'left', left_on='team_h', right_on='id')
        #event_data = event_data[cols + ['name', 'strength_overall_home', 'strength_attack_home', 'strength_defence_home']]
        event_data.rename(columns={'short_name': 'team_h_name', 
                                   'strength_overall_away':'team_h_strength_overall',
                                   'strength_attack_away':'team_h_strength_attack',
                                   'strength_defence_away':'team_h_strength_defence'
                                  }, inplace=True)
        event_data['team_a_difficulty_attack'] = event_data['team_a_strength_attack'] - event_data['team_h_strength_defence']
        event_data['team_a_difficulty_defence'] = event_data['team_a_strength_defence'] - event_data['team_h_strength_attack']
        event_data['team_h_difficulty_attack'] = event_data['team_h_strength_attack'] - event_data['team_a_strength_defence']
        event_data['team_h_difficulty_defence'] = event_data['team_h_strength_defence'] - event_data['team_a_strength_attack']
        event_data = pd.merge(event_data, gameweekInfo, how = 'left', left_on='event', right_on='id')
        event_data = event_data[cols]
        event_data['deadline_time'] = event_data[['deadline_time']].apply(lambda x: datetime.datetime.strptime(x['deadline_time'], '%Y-%m-%dT%H:%M:%SZ'), axis = 1)

        return event_data
    
    def getNextFDRDetails(self, teams = [], n=3):
            
        gameweekInfo = self.getGameWeekInfo()
        if n > 0:
            eventFDR = [self.getEventFDR(i+1) for i in range(self.currentGw, self.currentGw + n)]
        else:
            eventFDR = [self.getEventFDR(self.currentGw + n)]
        fdrResult = pd.concat(eventFDR)
        
        if (self.save):
            self.saveLog(fdrResult, 'fixture_details')

        if teams:
            fdrResult = fdrResult[(fdrResult['team_a_name'].isin(teams) | fdrResult['team_h_name'].isin(teams) )]
            
        return fdrResult
    
    def getNextFDRSummary(self, teams = [], n = 3):
        
        details = self.getNextFDRDetails(teams, n)
        teams = set(list(details['team_a_name']) + list(details['team_h_name']))
        result = pd.DataFrame()
        for team in teams:
            fix = details[(details['team_a_name'].isin([team]) | details['team_h_name'].isin([team]))]
            fix['team'] = team
            fix['opp'] = fix[['team_a_name', 'team_h_name']].apply(lambda x, team: x['team_a_name'] if x['team_h_name'] == team else x['team_h_name'], axis= 1, team = team)
            fix['fdr_attack_strength'] = fix[['team_h_difficulty_attack', 'team_a_difficulty_attack', 'team_h_name']].apply(lambda x, team: x['team_h_difficulty_attack'] if x['team_h_name'] == team else x['team_a_difficulty_attack'], axis= 1, team = team)
            fix['fdr_defence_strength'] = fix[['team_h_difficulty_defence', 'team_a_difficulty_defence', 'team_h_name']].apply(lambda x, team: x['team_h_difficulty_defence'] if x['team_h_name'] == team else x['team_a_difficulty_defence'], axis= 1, team = team)
            fix = fix.groupby(by = ['team']).agg( {
                    'opp': ', '.join,
                    'fdr_attack_strength': 'mean',
                    'fdr_defence_strength': 'mean'
                })
            result = pd.concat([result, fix])
            
        result['fdr_attack_scale'] = round(5*(result['fdr_attack_strength'] - result['fdr_attack_strength'].min())/(result['fdr_attack_strength'].max() - result['fdr_attack_strength'].min()),0)
        result['fdr_defence_scale'] = round(5*(result['fdr_defence_strength'] - result['fdr_defence_strength'].min())/(result['fdr_defence_strength'].max() - result['fdr_defence_strength'].min()),0)

        return result
        
    
    def getPlayerSummary(self, playerTypeCode=None, id=None, excludeZeroPoints = True, includeNextFixtures = 3):

        raw_data = self.getStaticRawData()
        teams = self.getLatestRatings()
        
        # Cols
        fpl_stat_cols = ['dreamteam_count', 'cost_change_start_fall', 'selected_by_percent', 'transfers_in_event', 'transfers_out_event', 'form', 'value_form', 'value_season']
        basic_info_cols = ['id', 'first_name', 'second_name', 'team', 'web_name', 'element_type', 'now_cost']
        game_stats = [z['name'] for z in raw_data['element_stats']]
        extra_stats = ['matches', 'points_per_game', 'event_points', 'total_points', 'corners_and_indirect_freekicks_order', 'direct_freekicks_order', 'penalties_order']
        summaryCols = ['element', 'web_name', 'short_name', 'first_name', 'second_name', 'now_cost', 'element_type', 'status', 'news'] + game_stats + extra_stats + fpl_stat_cols + ['strength_attack_home', 'strength_attack_away', 'strength_defence_home', 'strength_defence_away']
        playerCols = basic_info_cols + game_stats + extra_stats + fpl_stat_cols + ['status', 'news']

        playerInfo = pd.DataFrame(raw_data['elements'])
        playerInfo.fillna(0, inplace = True)
        playerInfo['matches'] = playerInfo[['total_points','points_per_game']].apply(lambda x: round(float(x['total_points']) / float(x['points_per_game']),0) if float(x['points_per_game']) > 0 else 0, axis = 1)
        
        if (self.save):
            self.saveLog(playerInfo, 'player_details')
            
        playerInfo = playerInfo[playerCols]

        #filters
        if id is not None: playerInfo = playerInfo[playerInfo['id'].isin(id)]
        if excludeZeroPoints: playerInfo = playerInfo[playerInfo['total_points'] > 0]
        
        playerInfo = playerInfo.rename(columns={'id':'element'})
        combPlayerInfo = pd.merge(playerInfo,teams, how = 'inner', left_on='team', right_on='id')

        if playerTypeCode is not None:
            combPlayerInfo = combPlayerInfo[combPlayerInfo['element_type'] == playerTypeCode]

        combPlayerInfo = combPlayerInfo[summaryCols]
        combPlayerInfo = combPlayerInfo.sort_values(by = ['total_points'], ascending=False)
        
        if includeNextFixtures > 0:
            nextFixDetails = self.getNextFDRSummary([],includeNextFixtures)
            combPlayerInfo = combPlayerInfo.merge(nextFixDetails, how = 'left', left_on='short_name', right_on='team')
        
        understats = self.getPlayerUnderStats()
        understats['understats'] = True
        combPlayerInfo['full_name'] = combPlayerInfo[['first_name', 'second_name']].apply(lambda x: x['first_name'] + ' ' + x['second_name'], axis =1)
        combPlayerInfo = pd.merge(combPlayerInfo, understats, how='left', left_on='full_name', right_on='player_name')

        if excludeZeroPoints: combPlayerInfo = self.addAdditionalPlayerStats(combPlayerInfo)

        combPlayerInfo.fillna(0, inplace = True)
        return combPlayerInfo

    def addAdditionalPlayerStats(self, players):
        players['xG90'] = players['xG'].astype(float)*90/players['minutes']
        players['xA90'] = players['xA'].astype(float)*90/players['minutes']
        players['shots90'] = players['shots'].astype(float)*90/players['minutes']
        players['key_passes90'] = players['key_passes'].astype(float)*90/players['minutes']
        players['npg90'] = players['npg'].astype(float)*90/players['minutes']
        players['npxG90'] = players['npxG'].astype(float)*90/players['minutes']
        players['xGChain90'] = players['xGChain'].astype(float)*90/players['minutes']
        players['xGBuildup90'] = players['xGBuildup'].astype(float)*90/players['minutes']
        players['goals_scored90'] = players['goals_scored']*90/players['minutes']
        players['assists90'] = players['assists']*90/players['minutes']
        players['bps90'] = players['bps']*90/players['minutes']
        players['goals_diff90'] = players['goals_scored90'] - players['xG90']
        players['assist_diff90'] = players['assists90'] - players['xA90']
        players['pg90'] = players['goals_scored90'] - players['npg90']
        players['pgxG90'] = players['xG90'] - players['npxG90']

        return players

    
    def getPlayerDetails(self, playerIds = None):
    
        playerSummary = self.getPlayerSummary(excludeZeroPoints = False)[['element', 'web_name', 'short_name']]
        if playerIds:
            playerSummary = playerSummary[playerSummary['element'].isin(playerIds)]

        playerIds = set(playerSummary.element)
        playerDetails = pd.DataFrame()
        for id in playerIds:
            url = self.url_player_details + str(id) + '/'
            raw_data = requests.get(url).json()
            raw_data = pd.DataFrame(raw_data['history'])
            raw_data.fillna(0, inplace = True)
            playerDetails = pd.concat([playerDetails, raw_data])

        combPlayerdetails = pd.merge(playerDetails, playerSummary, how = 'inner', left_on='element', right_on='element')

        return combPlayerdetails
    
    def getPlayerPastSeasonSummary(self, playerIds = None):
        
        playerSummary = self.getPlayerSummary(excludeZeroPoints = False)[['element', 'web_name', 'short_name']]
        if playerIds:
            playerSummary = playerSummary[playerSummary['element'].isin(playerIds)]

        playerIds = set(playerSummary.element)
        playerDetails = pd.DataFrame()
        for id in playerIds:
            url = self.url_player_details + str(id) + '/'
            raw_data = requests.get(url).json()
            raw_data = pd.DataFrame(raw_data['history_past'])
            raw_data['element'] = id
            raw_data.fillna(0, inplace = True)
            playerDetails = pd.concat([playerDetails, raw_data])

        combPlayerdetails = pd.merge(playerDetails, playerSummary, how = 'inner', left_on='element', right_on='element')

        return combPlayerdetails

    def findPlayer(self, pattern):
        
        players = [p.strip() for p in pattern.split(',')]
        stats = self.getPlayerSummary()
        stats['web_name_decode'] = stats[['web_name']].apply(lambda x: unidecode.unidecode(x['web_name']), axis = 1)
        stats['full_name_decode'] = stats[['full_name']].apply(lambda x: unidecode.unidecode(x['full_name']), axis = 1)
        
        result = pd.DataFrame()
        for p in players:
            df = stats[stats['web_name_decode'].str.lower() == p.lower()]
            if df.shape[0] == 0:
                df = stats[stats['web_name_decode'].str.match(p, flags=re.IGNORECASE)]
            if df.shape[0] == 0:
                df = stats[stats['full_name_decode'].str.match(p, flags=re.IGNORECASE)]
            if df.shape[0] == 0:
                df = stats[stats['web_name_decode'].str.contains(p, flags=re.IGNORECASE, regex=True)]
            result = pd.concat([result, df])
        return result

    def getPlayerUnderStats(self):
        cols = ['player_name', 'xG', 'xA', 'shots', 'key_passes', 'npg', 'npxG', 'xGChain', 'xGBuildup']
        try:
            obj = GetStats()
            obj.get_league_players()
            understats = obj.players[['player_name', 'xG', 'xA', 'shots', 'key_passes', 'npg', 'npxG', 'xGChain', 'xGBuildup']]
            return understats
        except:
            return pd.DataFrame(columns = cols)

    def getEventDetails(self, eventId):

        url = self.url_fixture_stats + str(eventId)
        event_data_raw = requests.get(url).json()
        event_data = pd.DataFrame(event_data_raw)

        return event_data

    def calcNewRatings(self, current_rating, current_gw_info):

        exp_factor = .25
    
        teams = current_rating.copy(deep = True)
        team_stat_gw = current_gw_info.copy(deep = True)
        team_stat_gw = team_stat_gw[['team_a', 'team_a_score', 'team_h', 'team_h_score']]
        
        cols = teams.columns
        
        team_stat_gw = team_stat_gw.merge(teams[['id', 'strength_attack_away', 'strength_defence_away']], how = 'left', left_on='team_a', right_on='id')
        team_stat_gw = team_stat_gw.merge(teams[['id', 'strength_attack_home', 'strength_defence_home']], how = 'left', left_on='team_h', right_on='id')
        
        # Calculate Factors
        team_stat_gw['factor_attack_away'] = ((team_stat_gw['strength_attack_away'] - ((team_stat_gw['strength_attack_away'] + team_stat_gw['strength_defence_home'])/2)))/3
        team_stat_gw['factor_attack_home'] = ((team_stat_gw['strength_attack_home'] - ((team_stat_gw['strength_attack_home'] + team_stat_gw['strength_defence_away'])/2)))/3
        team_stat_gw['factor_defence_away'] = ((team_stat_gw['strength_defence_away'] - ((team_stat_gw['strength_defence_away'] + team_stat_gw['strength_attack_home'])/2)))/3
        team_stat_gw['factor_defence_home'] = ((team_stat_gw['strength_defence_home'] - ((team_stat_gw['strength_defence_home'] + team_stat_gw['strength_attack_away'])/2)))/3


        # Calculate New Scores
        team_stat_gw['strength_attack_away_new'] = team_stat_gw[['factor_attack_away', 'team_a_score', 'strength_attack_away']].apply(
            lambda x:  abs(x['factor_attack_away']) * x['team_a_score'] +  x['strength_attack_away']
            if x['factor_attack_away'] < 0 else abs(x['factor_attack_away']) * (x['team_a_score'] - 3) +  x['strength_attack_away']
        , axis = 1)
        team_stat_gw['strength_attack_home_new'] = team_stat_gw[['factor_attack_home', 'team_h_score', 'strength_attack_home']].apply(
            lambda x:  abs(x['factor_attack_home']) * x['team_h_score'] +  x['strength_attack_home']
            if x['factor_attack_home'] < 0 else abs(x['factor_attack_home']) * (x['team_h_score'] - 3) +  x['strength_attack_home']
        , axis = 1)
        team_stat_gw['strength_defence_away_new'] = team_stat_gw[['factor_defence_away', 'team_h_score', 'strength_defence_away']].apply(
            lambda x:  -1* abs(x['factor_defence_away']) * x['team_h_score'] +  x['strength_defence_away']
            if x['factor_defence_away'] > 0 else abs(x['factor_defence_away']) * (3 - x['team_h_score'] ) +  x['strength_defence_away']
        , axis = 1)
        team_stat_gw['strength_defence_home_new'] = team_stat_gw[['factor_defence_home', 'team_a_score', 'strength_defence_home']].apply(
            lambda x:  -1* abs(x['factor_defence_home']) * x['team_a_score'] +  x['strength_defence_home']
            if x['factor_defence_home'] > 0 else abs(x['factor_defence_home']) * (3 - x['team_a_score'] ) +  x['strength_defence_home']
        , axis = 1)

        team_stat_gw['strength_attack_away_new'] = exp_factor*team_stat_gw['strength_attack_away_new'] + (1-exp_factor) *team_stat_gw['strength_attack_away']
        team_stat_gw['strength_attack_home_new'] = exp_factor*team_stat_gw['strength_attack_home_new'] + (1-exp_factor) *team_stat_gw['strength_attack_home']
        team_stat_gw['strength_defence_away_new'] = exp_factor*team_stat_gw['strength_defence_away_new'] + (1-exp_factor) *team_stat_gw['strength_defence_away']
        team_stat_gw['strength_defence_home_new'] = exp_factor*team_stat_gw['strength_defence_home_new'] + (1-exp_factor) *team_stat_gw['strength_defence_home']
        
        # transform original rating df
        teams = teams.merge(team_stat_gw[['team_a', 'strength_attack_away_new', 'strength_defence_away_new']], how = 'left', left_on='id', right_on='team_a')
        teams = teams.merge(team_stat_gw[['team_h', 'strength_attack_home_new', 'strength_defence_home_new']], how = 'left', left_on='id', right_on='team_h')
        teams.fillna(0, inplace = True)
        teams['strength_attack_away_new'] = teams[['strength_attack_away', 'strength_attack_away_new']].apply(lambda x: x['strength_attack_away_new'] if x['strength_attack_away_new'] else x['strength_attack_away'], axis = 1)
        teams['strength_attack_home_new'] = teams[['strength_attack_home', 'strength_attack_home_new']].apply(lambda x: x['strength_attack_home_new'] if x['strength_attack_home_new'] else x['strength_attack_home'], axis = 1)
        teams['strength_defence_away_new'] = teams[['strength_defence_away', 'strength_defence_away_new']].apply(lambda x: x['strength_defence_away_new'] if x['strength_defence_away_new'] else x['strength_defence_away'], axis = 1)
        teams['strength_defence_home_new'] = teams[['strength_defence_home', 'strength_defence_home_new']].apply(lambda x: x['strength_defence_home_new'] if x['strength_defence_home_new'] else x['strength_defence_home'], axis = 1)

        # Rename Cols
        teams['strength_attack_away'] = teams['strength_attack_away_new']
        teams['strength_attack_home'] = teams['strength_attack_home_new']
        teams['strength_defence_away'] = teams['strength_defence_away_new']
        teams['strength_defence_home'] = teams['strength_defence_home_new']

        return teams[cols]

    def getLatestRatings(self, current_gw = None):
        teams = self.getTeamDetails()
        current_gw = min(current_gw, self.getCurerntGameWeek()) if current_gw else self.getCurerntGameWeek()

        for event in range(1,current_gw + 1):
            current_gw_info = self.getEventDetails(event)
            current_gw_info = current_gw_info[current_gw_info['finished_provisional'] == True]
            if len(current_gw_info):
                teams = self.calcNewRatings(teams, current_gw_info)
        return teams
    
    def comparePlayers(self, player1, player2, features = None, filename = None):
        if features is None:
            features = ['pgxG90',
                        'pg90',
                        'npxG90',
                        'npg90',
                        'xG90',
                        'goals_scored90',
                        'xA90',
                        'assists90',
                        'xGChain90', 
                        'xGBuildup90',
                        'shots90', 
                        'key_passes90',
                        'goals_diff90', 
                        'assist_diff90',
                        'bps90']

        try:
            player1Det = [p.strip() for p in player1.split("+")]
            player2Det = [p.strip() for p in player2.split("+")]
            
            if len(player1Det) == 1 and len(player2Det) == 1:
                players = self.findPlayer(player1 + ',' + player2)
            else:
                players = pd.DataFrame()
                for player in [player1Det, player2Det]:
                    temp = self.findPlayer(",".join(player))
                    if temp.shape[0] == len(player):
                        temp['group'] = "+".join(list(temp['web_name'].values))
                        players = pd.concat([players, temp])
                players = players[['web_name', 'group'] + features]
                players = players.groupby(by = ["group"]).sum()
                players.reset_index(inplace = True)
                players.rename(columns = {"group" : "web_name"}, inplace=True)
            
        except:
            players = self.findPlayer(player1 + ',' + player2)

        if players.shape[0] == 2:
            N = len(features)
            players = players[['web_name'] + features]
            players.reset_index(inplace = True, drop = True)
            
            # Normalize
            df = players.copy(deep = True)
            df.iloc[:,1:] = df.iloc[:,1:]/df.iloc[:,1:].max()

            angles = [n / float(N) * 2 * pi for n in range(N)]
            angles += angles[:1]
            #ax = plt.subplot(111, polar=True)
            fig = plt.figure()
            ax = fig.add_subplot(111, polar=True)
            ax.set_theta_offset(pi / 2)
            ax.set_theta_direction(-1)
            plt.xticks(angles[:-1], features)

            values=df.loc[0].drop('web_name').values.flatten().tolist()
            values += values[:1]
            ax.plot(angles, values, linewidth=1, linestyle='solid', label=df.loc[0]['web_name'])
            ax.fill(angles, values, 'b', alpha=0.1)

            values=df.loc[1].drop('web_name').values.flatten().tolist()
            values += values[:1]
            ax.plot(angles, values, linewidth=1, linestyle='solid', label=df.loc[1]['web_name'])
            ax.fill(angles, values, 'r', alpha=0.1)

            plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
            if filename:
                fig.savefig(filename + '.png')
                plt.close(fig)
        
        return players
