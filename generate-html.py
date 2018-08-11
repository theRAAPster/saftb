import mysql.connector as mariadb
import os

try:
    saftb_db_host = os.environ["saftb_db_host"]
    saftb_db_user = os.environ["saftb_db_user"]
    saftb_db_password = os.environ["saftb_db_password"]
    saftb_db_database = os.environ["saftb_db_database"]
except KeyError:
    print("Please set the required environment variables")
    exit(1)

mariadb_connection = mariadb.connect(host=saftb_db_host, user=saftb_db_user, password=saftb_db_password, database=saftb_db_database)
cursor = mariadb_connection.cursor()

#get all pickers
try:
    cursor.execute("SELECT id,team_name FROM pickers;")
except mariadb.Error as error:
    print("Error: {}".format(error))

pickers = cursor.fetchall()

scores = {}

for id, team_name in pickers:
    scores[team_name] = []
    try:
        cursor.execute("select short_name, points from picks inner join api_teams t on (picks.team_id=t.id) inner join api_standings s on (t.api_id=s.team_api_id) where picks.season_id = 1 and pickers_id = %(pickers_id)s order by pick_number;", { 'pickers_id': id})
    except mariadb.Error as error:
        print("Error: {}".format(error))

    teams = cursor.fetchall()
    
    for short_name, points in teams:
        scores[team_name].append([short_name, points])

mariadb_connection.close()

points = {}

for row in scores:
    sum = 0
    for team in scores[row]:
        sum += team[1]
    points[row] = sum

print("""<html>
<head>
 <title>SAFTB - EPL</title>
</head>
<body>
<table border="1">""")

print("<tr><th>Team</th><th>Pick 1</th><th>Pick 2</th><th>Pick 3</th><th>Pick 4</th><th>Pick 5</th><th>Points</th></tr>")

for team in sorted(points, key=points.get, reverse=True):
    print("<tr><td>{}</td><td>{} ({})</td><td>{} ({})</td><td>{} ({})</td><td>{} ({})</td><td>{} ({})</td><td>{}</td></tr>".format( team,
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
                                                                                                                                    points[team]))

print("""</table>
</body></html>""")