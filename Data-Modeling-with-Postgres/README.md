# Schema for Song Play Analysis

## Summary
The purpose of this database is to understand what, where and how each user is listening to the songs in Sparkify. The analytial goals is to find out what is making the free tier users switch to paid tier and why paid users are downgrading to free tier through their listening habits.

## How to run the Python scripts
1. `create_tables.py` will create the database and tables, dropping any tables with conflicting names beforehand.

1. `etl.py` reads and processes files from `data/song_data` and `data/log_data` and loads them into the 5 tables.

## Database schema design
We have 4 dimension tables (users, songs, artists, time) and 1 fact table (songplays).

- users: Stores the information of each unique users using the app
  - If users change their info, the users table will allow changes without error
  - user_id as `PRIMARY KEY`, each user_id is associated with only one user
- songs: Stores the information of each unique songs in the music database
  - song's information cannot be alterd once created as it should stay the same
  - song_id as `PRIMARY KEY`, each song_id is associated with only one song
- artists: Stores the information of each unique artists in the music database
  - If artist's info is changed, their location would be updated without error
  - artist_id as `PRIMARY KEY`, each artist_id is associated with only one artist
- time: timestamps of records in songplays broken down into specific units
  - This allows us to better understand what period of the day/week/month/year do people listen to music
  - start_time as `PRIMARY KEY`, each record requires a start_time to initialize the date time record
  
- songplay: Stores information of each song played in the logs data
  - Aggregates the crucial information of what and when the user is listening
  - songplay_id as `SERIAL PRIMARY KEY`, for each record the id will increment automatically as each record is unique

## ETL pipeline
- Extract data from `data/song_data`
- Transform the data into `artists` and `songs`
- Load the data into its respective tables

- Extract data from `data/log_data`
- Transform the data to show additional information regarding date and time
- Load the data into its respective tables

- Combine data from `artists`, `songs`, `users`, `time` to `songsplay` table 

## Files in the repository
- data: contains log and song data
- create_tables.py: run this file to reset the tables before each time the ETL script runs
- etl.ipynb: Testing code to read and processes a single file from song_data and log_data and loads the data into the tables
- etl.py: reads and processes files from song_data and log_data and loads them into your tables
- sql_queries.py: contains all sql queries, and is imported into the last three files above
- test.ipynb: check the data inside the tables in the database to make sure the code is working properly

## Example queries and results for song play analysis.

`SELECT user_id, count(*) FROM songplays where level = 'paid' group by user_id order by count desc limit 5;`

| user_id | count |
|---------|-------|
| 49      | 689   |
| 80      | 665   |
| 97      | 557   |
| 15      | 463   |
| 44      | 397   |
