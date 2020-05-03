# Data Modeling with Cassandra

## Summary
1. Processed the csv files from `event_data` to create a single csv file that will be used for Apache Casssandra tables
1. Querying data through Apache Cassandra
    - Created Cassandra Cluster and Keyspace
    - Created a new table for each specific query
    - Load data into each table from the aggregated file, `event_datafile_new.csv`
    - Utilized Primary Key (includes Partition Key and Clustering columns) to query

## ETL Pipeline Processing
- Combine all csv files from `event_data` into one single csv file `event_datafile_new.csv`
- The image below is a screenshot of what the denormalized data appear like

![](image_event_datafile_new.jpg)

## Data Modeling
- Created the Apache Cassandra tables for ***three queries***
- The CREATE TABLE statement includes the appropriate datatype and unique names
- Table names reflect the query and the result it will generate
- Created one table per query, following the rules of Apache Cassandra
- Implemented PRIMARY KEY with a COMPOSITE Partition for both the CREATE and INSERT statements
- The SELECT statement does **NOT** use `ALLOW FILTERING` to generate the results

### Primary Keys
- Apache Cassandra is a partition row store, the partition key determines which node a particular row is stored on
- The combination of the PARTITION KEY and CLUSTERING COLUMNS are used to uniquely identify each row
- With the Primary key (Partition Key and Clustering columns), the partitions are distributed across the nodes of the cluster
- The sequence in which columns appear reflect how the data is partitioned and the order of the data within the partitions
- Any clustering column(s) would determine the order in which the data is sorted within the partition

### Query 1
Find the artist, song title and song's length in the music app history that was heard during sessionId = 338, and itemInSession = 4

**Create Table 1**
```SQL
CREATE TABLE IF NOT EXISTS artists_songs_info (
    sessionId INT, itemInSession INT, artist VARCHAR, 
    song VARCHAR, length DECIMAL, 
    PRIMARY KEY (sessionId, itemInSession))
```
- Each row is uniquely identified with the combination of userId, sessionId and clustering column itemInSession

**Query 1**
```SQL
SELECT artist, song, length
FROM artists_songs_info
WHERE sessionId = 338 AND itemInSession = 4
```

|   | artist    | song                            | length   |
|---|-----------|---------------------------------|----------|
| 0 | Faithless | Music Matters (Mark Knight Dub) | 495.3073 |

### Query 2
Find the name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182

**Create Table**
```MySQL
CREATE TABLE IF NOT EXISTS artists_songs_users_info (
    userId INT, sessionId INT, itemInSession INT, artist VARCHAR, 
    song VARCHAR, firstName VARCHAR, lastName VARCHAR,
    PRIMARY KEY (userId, sessionId, itemInSession))
```
**Query 2**
```SQL
SELECT artist, song, firstName, lastName
FROM artists_songs_users_info
WHERE userId = 10 AND sessionId = 182
```

|   | artist            | song                                              | firstname | lastname |
|---|-------------------|---------------------------------------------------|-----------|----------|
| 0 | Down To The Bone  | Keep On Keepin' On                                | Sylvie    | Cruz     |
| 1 | Three Drives      | Greece 2000                                       | Sylvie    | Cruz     |
| 2 | Sebastien Tellier | Kilometer                                         | Sylvie    | Cruz     |
| 3 | Lonnie Gordon     | Catch You Baby (Steve Pitron & Max Sanna Radio... | Sylvie    | Cruz     |

### Query 3
Find every user name (first and last) in the data who listened to the song 'All Hands Against His Own'

**Create Table**
```MySQL
CREATE TABLE IF NOT EXISTS users_songs_table (
    song VARCHAR, userId INT, 
    firstName VARCHAR, lastName VARCHAR, 
    PRIMARY KEY (song, userId))
```
- SELECT statement selected only the name of the user, even though the data in the table is partitioned with a PARTITION KEY and CLUSTERING COLUMN for this specific query

**Query 3**
```MySQL
SELECT firstName, lastName
FROM users_songs_table
WHERE song = 'All Hands Against His Own'
```

|   | firstname  | lastname |
|---|------------|----------|
| 0 | Jacqueline | Lynch    |
| 1 | Tegan      | Levine   |
| 2 | Sara       | Johnson  |

