import config #credentials in a separate file
import pandas as pd
from sqlalchemy import create_engine
from nba_api.stats.endpoints import playergamelog, commonplayerinfo

#connect to local postgresql database using credentials from config
engine = create_engine('postgresql://' + config.username + ':' 
                       + config.pwd +'@' + config.hostname +':' 
                       + config.port_id + '/' + config.database)

#grabs all the active season_ids 
info = commonplayerinfo.CommonPlayerInfo(player_id=201939)
season_ids = info.available_seasons.get_data_frame()
active_seasons = []

#if season_id begins with a 2, it means its a regular season
for i in season_ids['SEASON_ID']:
    if i[0] == '2': #grabs all the regular season in year
        active_seasons.append(i[1:])

for n in active_seasons:
    #grabs player log
    data = playergamelog.PlayerGameLog(player_id='201939', season=n, season_type_all_star='Regular Season')
    df = data.player_game_log.get_data_frame()

    df.to_sql("season_" + str(n), engine, if_exists='replace') #upload table to database

print('Tables Updated!')
engine.dispose()