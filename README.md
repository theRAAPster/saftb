Collection of random things to track EPL scoring until I can get better organized.

Python note requirements:
pip freeze > requirements.txt

Python install requirements:
pip install -r requirements.txt

Set env variable for python virtual environment (OS X):
export SAFTB_PYTHON_LOC=env/bin/python

Set env variable for python virtual environment (Windows):
setx SAFTB_PYTHON_LOC "env\\Scripts\\python.exe"

docker run --name mariadb -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 -d mariadb:10.3.8
docker exec -it mariadb bash

Run sql1.sql  
Run get-teams.py  
Run get-standings.py  
Run sql2.sql  
Run generate-html.py  