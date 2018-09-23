Collection of random things to track EPL scoring until I can get better organized.

docker run --name mariadb -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mariadb:10.3.8
docker exec -it mariadb bash

Run sql1.sql
Run get-teams.py
Run get-standings.py
Run sql2.sql
Run get-standings.py
Run generate-html.py