import mysql.connector as mariadb
from mysql.connector import errorcode
import os
from datetime import datetime
import time
import requests

try:
    api_token = os.environ["api_token"]
    saftb_db_host = os.environ["saftb_db_host"]
    saftb_db_user = os.environ["saftb_db_user"]
    saftb_db_password = os.environ["saftb_db_password"]
    saftb_db_database = os.environ["saftb_db_database"]
except KeyError:
    print("Please set the required environment variables")
    exit(1)

DB_NAME = 'dbo'

TABLES = {}
TABLES['api_seasons'] = (
    "CREATE TABLE `api_seasons` ("
    "   `id`                INT NOT NULL AUTO_INCREMENT ,"
    "   `api_id`            INT NOT NULL ,"
    "   `start_date`        DATE NOT NULL ,"
    "   `end_date`          DATE NOT NULL ,"
    "   `current_match_day` INT NOT NULL ,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
)

TABLES['api_standings'] = (
    "CREATE TABLE `api_standings` ("
    "   `id`              INT NOT NULL AUTO_INCREMENT ,"
    "   `team_api_id`     INT NOT NULL ,"
    "   `position`        INT NOT NULL ,"
    "   `played_games`    INT NOT NULL ,"
    "   `won`             INT NOT NULL ,"
    "   `draw`            INT NOT NULL ,"
    "   `lost`            INT NOT NULL ,"
    "   `points`          INT NOT NULL ,"
    "   `goals_for`       INT NOT NULL ,"
    "   `goals_against`   INT NOT NULL ,"
    "   `goal_difference` INT NOT NULL ,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
)

TABLES['api_teams'] = (
    "CREATE TABLE `api_teams` ("
    "   `id`               INT NOT NULL AUTO_INCREMENT ,"
    "   `api_id`           INT NOT NULL ,"
    "   `area`             VARCHAR(45) ,"
    "   `name`             VARCHAR(45) NOT NULL ,"
    "   `short_name`       VARCHAR(45) NOT NULL ,"
    "   `tla`              VARCHAR(45) ,"
    "   `address`          VARCHAR(90) ,"
    "   `phone`            VARCHAR(45) ,"
    "   `website`          VARCHAR(45) ,"
    "   `email`            VARCHAR(45) ,"
    "   `founded`          INT ,"
    "   `club_colors`      VARCHAR(45) ,"
    "   `venue`            VARCHAR(45) ,"
    "   `api_last_updated` DATETIME NOT NULL ,"
    "   `crest_url`        VARCHAR(250) ,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
)

TABLES['pickers'] = (
    "CREATE TABLE `pickers` ("
    "   `id`              INT NOT NULL AUTO_INCREMENT ,"
    "   `season_id`       INT NOT NULL ,"
    "   `team_name`       VARCHAR(45) NOT NULL ,"
    "   `team_short_name` VARCHAR(45) NOT NULL ,"
    "   `draft_order`     INT NOT NULL ,"
    "   PRIMARY KEY (`id`, `season_id`),"
    "   KEY `fkIdx_68` (`season_id`),"
    "   CONSTRAINT `FK_68` FOREIGN KEY `fkIdx_68` (`season_id`) REFERENCES `api_seasons` (`id`)"
    ") ENGINE=InnoDB"
)

TABLES['picks'] = (
    "CREATE TABLE `picks` ("
    "   `id`          INT NOT NULL AUTO_INCREMENT ,"
    "   `pickers_id`  INT NOT NULL ,"
    "   `season_id`   INT NOT NULL ,"
    "   `team_id`     INT NOT NULL ,"
    "   `pick_number` INT NOT NULL ,"
    "   PRIMARY KEY (`id`, `pickers_id`, `season_id`, `team_id`),"
    "   KEY `fkIdx_81` (`pickers_id`, `season_id`),"
    "   CONSTRAINT `FK_81` FOREIGN KEY `fkIdx_81` (`pickers_id`, `season_id`) REFERENCES `dbo`.`pickers` (`id`, `season_id`),"
    "   KEY `fkIdx_86` (`team_id`),"
    "   CONSTRAINT `FK_86` FOREIGN KEY `fkIdx_86` (`team_id`) REFERENCES `dbo`.`api_teams` (`id`)"
    ") ENGINE=InnoDB"
)

mariadb_connection = mariadb.connect(host=saftb_db_host, user=saftb_db_user, password=saftb_db_password)
cursor = mariadb_connection.cursor()

# Create Database if it does not exist
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mariadb.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mariadb.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        mariadb_connection.database = DB_NAME
    else:
        print(err)
        exit(1)

# Create tables
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mariadb.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

# Start putting data in
try:
    print("Adding data to api_seasons table: ", end='')
    cursor.execute("INSERT INTO api_seasons (api_id, start_date, end_date, current_match_day) VALUES (%s,%s,%s,%s)", 
                (168, '2019-08-09', '2020-05-17', 1))
except mariadb.Error as err:
    print(err)
    exit(1)
else:
    print("OK")

try:
    print("Adding data to pickers table: ", end='')
    cursor.execute("INSERT INTO pickers (season_id, team_name, team_short_name, draft_order) VALUES (%s,%s,%s,%s)", 
                (1, 'Cole/Raap', 'C/R', 1))
    cursor.execute("INSERT INTO pickers (season_id, team_name, team_short_name, draft_order) VALUES (%s,%s,%s,%s)", 
                (1, 'Jeff/Grego', 'J/G', 2))
    cursor.execute("INSERT INTO pickers (season_id, team_name, team_short_name, draft_order) VALUES (%s,%s,%s,%s)", 
                (1, 'Logan/Ferg', 'L/F', 3))
    cursor.execute("INSERT INTO pickers (season_id, team_name, team_short_name, draft_order) VALUES (%s,%s,%s,%s)", 
                (1, 'Trella/Jarrod', 'T/J', 4))
except mariadb.Error as err:
    print(err)
    exit(1)
else:
    print("OK")

###########
# api_teams
###########
url = 'http://api.football-data.org/v2/competitions/2021/teams'
headers = {'X-Auth-Token': api_token}
r = requests.get(url, headers=headers)

if r.status_code == 200:

    print("Adding data to api_teams table: ", end='')
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
        except mariadb.Error as err:
            print(err)
            exit(1)

        mariadb_connection.commit()
        #print("The last inserted id was: ", cursor.lastrowid)
    print("OK")
###########
# end api_teams
###########

###########
# api_standings
###########
url = 'http://api.football-data.org/v2/competitions/2021/standings'
headers = {'X-Auth-Token': api_token}
r = requests.get(url, headers=headers)

if r.status_code == 200:
    #truncate table before inserting records
    try:
        print("Truncating api_standings table: ", end='')
        cursor.execute("TRUNCATE TABLE api_standings")
    except mariadb.Error as err:
        print(err)
        exit(1)
    else:
        print("OK")

    mariadb_connection.commit()

    print("Updating crest URL and standings: ", end='')
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
                except mariadb.Error as err:
                    print(err)
                    exit(1)

                mariadb_connection.commit()

                #insert information
                try:
                    cursor.execute("INSERT INTO api_standings (team_api_id,position,played_games,won,draw,lost,points,goals_for,goals_against,goal_difference) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                        (team_api_id,position,played_games,won,draw,lost,points,goals_for,goals_against,goal_difference))
                except mariadb.Error as err:
                    print(err)
                    exit(1)

                mariadb_connection.commit()
                #print("The last inserted id was: ", cursor.lastrowid)
    print("OK")
###########
# end api_standings
###########

###########
# insert picks
###########
PICKS = []
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (1, 1, 6, 1)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (2, 1, 5, 2)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (3, 1, 1, 3)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (4, 1, 10, 4)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (4, 1, 3, 5)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (3, 1, 4, 6)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (2, 1, 7, 7)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (1, 1, 13, 8)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (1, 1, 11, 9)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (2, 1, 19, 10)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (3, 1, 15, 11)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (4, 1, 20, 12)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (4, 1, 14, 13)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (3, 1, 16, 14)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (2, 1, 2, 15)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (1, 1, 12, 16)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (1, 1, 8, 17)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (2, 1, 18, 18)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (3, 1, 9, 19)")
PICKS.append("INSERT INTO picks (pickers_id, season_id, team_id, pick_number) VALUES (4, 1, 17, 20)")

# Add picks
print("Adding picks to picks table: ", end='')
for pick in PICKS:
    try:
        cursor.execute(pick)
    except mariadb.Error as err:
        print(err)
        exit(1)

print("OK")

###########
# end insert picks
###########

###########
# print report
###########
#get all pickers
print("Generating report: ", end='')
try:
    cursor.execute("SELECT id,team_name FROM pickers;")
except mariadb.Error as err:
    print(err)
    exit(1)

pickers = cursor.fetchall()

scores = {}

for id, team_name in pickers:
    scores[team_name] = []
    try:
        cursor.execute("select short_name, points from picks inner join api_teams t on (picks.team_id=t.id) inner join api_standings s on (t.api_id=s.team_api_id) where picks.season_id = 1 and pickers_id = %(pickers_id)s order by pick_number;", { 'pickers_id': id})
    except mariadb.Error as err:
        print(err)
        exit(1)

    teams = cursor.fetchall()
    
    for short_name, points in teams:
        scores[team_name].append([short_name, points])

points = {}

for row in scores:
    sum = 0
    for team in scores[row]:
        sum += team[1]
    points[row] = sum

print("OK")

report = """<html>
<head>
 <title>SAFTB - EPL</title>
</head>
<body>
<table border="1">\n"""

report += "<tr><th>Team</th><th>Pick 1</th><th>Pick 2</th><th>Pick 3</th><th>Pick 4</th><th>Pick 5</th><th>Points</th></tr>\n"

for team in sorted(points, key=points.get, reverse=True):
    report += "<tr><td>{}</td><td>{} ({})</td><td>{} ({})</td><td>{} ({})</td><td>{} ({})</td><td>{} ({})</td><td>{}</td></tr>\n".format( team,
                                                                                                                                    scores[team][0][0],
                                                                                                                                    scores[team][0][1],
                                                                                                                                    scores[team][1][0],
                                                                                                                                    scores[team][1][1],
                                                                                                                                    scores[team][2][0],
                                                                                                                                    scores[team][2][1],
                                                                                                                                    scores[team][3][0],
                                                                                                                                    scores[team][3][1],
                                                                                                                                    scores[team][4][0],
                                                                                                                                    scores[team][4][1],
                                                                                                                                    points[team])

report += """</table>
</body>
<br />
<br />
<footer>
Last updated: {}
</footer>
</html>""".format(time.strftime("%Y-%m-%d %H:%M"))

try:
    print("Writing report to disk: ", end='')
    with open("frontend\\code\\index.html", "w") as report_file:
        report_file.write(report)
except IOError as err:
    print(err)
else:
    print("OK")

print(report)
###########
# end print report
###########

cursor.close()
mariadb_connection.close()