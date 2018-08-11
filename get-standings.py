import mysql.connector as mariadb
from datetime import datetime
import requests
import os

try:
    api_token = os.environ["api_token"]
    saftb_db_host = os.environ["saftb_db_host"]
    saftb_db_user = os.environ["saftb_db_user"]
    saftb_db_password = os.environ["saftb_db_password"]
    saftb_db_database = os.environ["saftb_db_database"]
except KeyError:
    print("Please set the required environment variables")
    exit(1)

url = 'http://api.football-data.org/v2/competitions/2021/standings'
headers = {'X-Auth-Token': api_token}
r = requests.get(url, headers=headers)

if r.status_code == 200:
    mariadb_connection = mariadb.connect(host=saftb_db_host, user=saftb_db_user, password=saftb_db_password, database=saftb_db_database)
    cursor = mariadb_connection.cursor()

    #truncate table before inserting records
    try:
        cursor.execute("TRUNCATE TABLE api_standings")
    except mariadb.Error as error:
        print("Error: {}".format(error))

    mariadb_connection.commit()

    for standing in r.json()['standings']:
        if standing['type'] == 'TOTAL':
            for place in standing['table']:
                position = place['position']
                team_api_id = place['team']['id']
                team_crest_url = place['team']['crestUrl']
                played_games = place['playedGames']
                won = place['won']
                draw = place['draw']
                lost = place['lost']
                points = place['points']
                goals_for = place['goalsFor']
                goals_against = place['goalsAgainst']
                goal_difference = place['goalDifference']

                #update Crest URL information
                try:
                    cursor.execute("UPDATE api_teams SET crest_url=%s WHERE api_id=%s", 
                        (team_crest_url,team_api_id))
                except mariadb.Error as error:
                    print("Error: {}".format(error))

                mariadb_connection.commit()

                #insert information
                try:
                    cursor.execute("INSERT INTO api_standings (team_api_id,position,played_games,won,draw,lost,points,goals_for,goals_against,goal_difference) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                        (team_api_id,position,played_games,won,draw,lost,points,goals_for,goals_against,goal_difference))
                except mariadb.Error as error:
                    print("Error: {}".format(error))

                mariadb_connection.commit()
                print("The last inserted id was: ", cursor.lastrowid)

    mariadb_connection.close()