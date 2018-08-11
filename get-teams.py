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

url = 'http://api.football-data.org/v2/competitions/2021/teams'
headers = {'X-Auth-Token': api_token}
r = requests.get(url, headers=headers)

if r.status_code == 200:
    mariadb_connection = mariadb.connect(host=saftb_db_host, user=saftb_db_user, password=saftb_db_password, database=saftb_db_database)
    cursor = mariadb_connection.cursor()

    for team in r.json()['teams']:
        api_id = team['id']
        area = team['area']['name']
        name = team['name']
        short_name = team['shortName']
        tla = team['tla']
        address = team['address']
        phone = team['phone']
        website = team['website']
        email = team['email']
        founded = team['founded']
        club_colors = team['clubColors']
        venue = team['venue']
        api_last_updated = team['lastUpdated']

        api_last_updated = datetime.strptime(api_last_updated, '%Y-%m-%dT%H:%M:%SZ')

        #insert information
        try:
            cursor.execute("INSERT INTO api_teams (api_id,area,name,short_name,tla,address,phone,website,email,founded,club_colors,venue,api_last_updated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                (api_id,area,name,short_name,tla,address,phone,website,email,founded,club_colors,venue,api_last_updated.strftime('%Y-%m-%d %H:%M:%S')))
        except mariadb.Error as error:
            print("Error: {}".format(error))

        mariadb_connection.commit()
        print("The last inserted id was: ", cursor.lastrowid)

    mariadb_connection.close()