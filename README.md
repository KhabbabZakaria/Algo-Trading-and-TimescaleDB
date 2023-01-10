# Algo-Trading-and-TimescaleDB
Getting Binance Trade Data and saving them in a TimescaleDB using Python and Docker

#First, we will pull the docker timescaledb image and run it:
```
docker pull timescale/timescaledb:latest-pg14 
docker run -d --name blah -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg14
```

#We need to install our Python modules. Remember, we need to install version 1.10.15 of python-binance, because the latest versions are buggy at least as of now and there is not much of an endeavour to fix them.
```
pip3 install python-binance==1.0.15
pip3 install python-decouple

pip3 install psycopg2-binary
```

#Create table in the container:
```
docker exec -it blah psql -U postgres
postgres=# CREATE TABLE IF NOT EXISTS raw_trade_data (
postgres(# time TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
postgres(# symbol text NOT NULL,
postgres(# price double PRECISION NOT NULL,
postgres(# quantity double PRECISION NOT NULL);
```
#Should give:
CREATE TABLE

#Check with:
```
postgres=# \dt
```
#Should give:
             List of relations
 Schema |      Name      | Type  |  Owner   
--------+----------------+-------+----------
 public | raw_trade_data | table | postgres
(1 row)

#Now create hyper table:
```
postgres=# SELECT create_hypertable('raw_trade_data', 'time');
```
#Should give:
      create_hypertable      
-----------------------------
 (1,public,raw_trade_data,t)
(1 row)


#After you run the main.py, you can check the data inside the container:
#Get data from time descendent max 10 at a time:
```
SELECT * from raw_trade_data ORDER BY time desc LIMIT 10;
```
#Output:
        time         | symbol |  price   | quantity 
---------------------+--------+----------+----------
 2023-01-10 12:16:40 | ETHBTC | 0.077198 |   0.3236
 2023-01-10 12:16:40 | ETHBTC | 0.077198 |   0.0186
 2023-01-10 12:16:39 | ETHBTC | 0.077198 |   0.1267
 2023-01-10 12:16:39 | ETHBTC | 0.077198 |   0.1019
 2023-01-10 12:16:34 | ETHBTC | 0.077198 |    0.075
 2023-01-10 12:16:34 | ETHBTC | 0.077198 |   0.0764
 2023-01-10 12:16:34 | ETHBTC | 0.077198 |   0.0755
 2023-01-10 12:16:34 | ETHBTC | 0.077198 |   0.0529
 2023-01-10 12:16:34 | ETHBTC | 0.077198 |   0.0229
 2023-01-10 12:16:34 | ETHBTC | 0.077198 |   0.0854
(10 rows)



