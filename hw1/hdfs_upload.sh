hdfs dfs -mkdir -p /user/hadoop/sports/football/raw
hdfs dfs -mkdir -p /user/hadoop/sports/football/cleaned

hdfs dfs -put -f ~/data/raw/*.csv /user/hadoop/sports/football/raw
hdfs dfs -put -f ~/data/cleaned/football_cleaned.csv /user/hadoop/sports/football/cleaned

hdfs dfs -ls -h /user/hadoop/sports/football/raw
hdfs dfs -ls -h /user/hadoop/sports/football/cleaned
hdfs dfs -du -h /user/hadoop/sports/football/cleaned
hdfs dfs -cat /user/hadoop/sports/football/cleaned/football_cleaned.csv | head