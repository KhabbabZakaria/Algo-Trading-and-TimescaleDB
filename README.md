# Algo-Trading-and-TimescaleDB
Getting Binance Trade Data and saving them in a TimescaleDB using Python and Docker

#First, we will pull the docker timescaledb image and run it:
```
docker pull timescale/timescaledb:latest-pg14 
docker run -d --name blah -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg14
```
