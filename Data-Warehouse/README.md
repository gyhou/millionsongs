# Schema for Song Play Analysis

## Summary
The purpose of this Redshift database is to understand what, where and how each user is listening to the songs in Sparkify. The analytial goals is to find out what is making the free tier users switch to paid tier and why paid users are downgrading to free tier through their listening habits.

## How to run the Python scripts
1. `create_tables.py` will create staging, fact, and dimension tables, dropping any tables with conflicting names beforehand.
1. `etl.py` loads data from S3 to staging tables, and transforms data into a set of dimensional tables.

## Database schema design
We have 2 staging tables (logs, songs), 1 fact table (songplays), and 4 dimension tables (users, songs, artists, time).

### Staging Tables
Load S3 bucket data into staging tables first then transform the data into smaller tables.

Data and Column type are modified as needed from `stl_load_errors` on Redshift query editor.
<br>
`select * from stl_load_errors`
- VARCHAR: string values
- FLOAT: floating-point numbers with decimals
- INTEGER: four-byte numbers (integers)
- BIGINT: eight-byte integers
No constraints on staging tables as they should be a clean copy of the source, so no filtering happening at this stage.
- staging_events: Stores entire data from 's3://udacity-dend/log_data'
- staging_songs: Stores entire data from 's3://udacity-dend/song_data'

### Fact Table
- songplay: Stores information of each song played in the logs data
  - Aggregates the crucial information of what and when the user is listening
  - songplay_id as `IDENTITY PRIMARY KEY`, for each record the id will increment automatically as each record is unique
  
### Dimension Tables
- users: Stores the information of each unique users using the app
  - user_id as `PRIMARY KEY`, each user_id is associated with only one user
- songs: Stores the information of each unique songs in the music database
  - song_id as `PRIMARY KEY`, each song_id is associated with only one song
- artists: Stores the information of each unique artists in the music database
  - artist_id as `PRIMARY KEY`, each artist_id is associated with only one artist
- time: timestamps of records in songplays broken down into specific units
  - This allows us to better understand what period of the day/week/month/year do people listen to music
  - start_time as `PRIMARY KEY`, each record requires a start_time to initialize the date time record

### Dealing with duplicate records
Since Redshift does not enforce uniqueness for any column, we have to implement additional queries to achieve distinct rows.
1. Locate and delete the duplicate rows
1. Create a new table to hold the distinct rows from old table
    - Delete new table data from old table
    - Append new table back to old table

## ETL pipeline
- Extract data from the S3 bucket
- Transform the data into `artists` and `songs`
- Load the data into its respective tables

- Extract data from `data/log_data`
- Transform the data to show additional information regarding date and time
- Load the data into its respective tables

- Combine data from `artists`, `songs`, `users`, `time` to `songsplay` table 

## Files in the repository
- create_tables.py: run this file to reset the tables before each time the ETL script runs
- etl.py: extracts data from S3, stages them in Redshift, and transforms data into a set of dimensional tables
- sql_queries.py: contains all sql queries, and is imported into the last two files above

## Example queries and results for song play analysis.

`SELECT user_id, count(*) FROM songplays where level = 'paid' group by user_id order by count desc limit 5;`

| **user_id | **count** |
|---------|-------|
| 49      | 650   |
| 80      | 648   |
| 97      | 557   |
| 15      | 462   |
| 44      | 397   |
