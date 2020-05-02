# Schema for Song Play Analysis

## Summary
The purpose of this database is to understand what, where and how each user is listening to the songs in Sparkify. The analytial goals is to find out what is making the free tier users switch to paid tier and why paid users are downgrading to free tier through their listening habits.

## How to run the Python scripts
1. `etl.py` loads data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional table parquet files.

## Database schema design
We have 1 fact table (songplays), and 4 dimension tables (users, songs, artists, time).

### Fact Table
- songplay: Stores information of each song played in the logs data
  - Aggregates the crucial information of what and when the user is listening
  - play_id as `PRIMARY KEY` added though `monotonically_increasing_id`, dropped any duplicates from the table as each record is unique
  - Partitioned by `year` and then `month`
  
### Dimension Tables
- users: Stores the information of each unique users using the app
  - user_id as `PRIMARY KEY`, dropped any duplicates from the table as each user_id is associated with only one user
- songs: Stores the information of each unique songs in the music database
  - song_id as `PRIMARY KEY`, dropped any duplicates from the table as each song_id is associated with only one song
  - Partitioned by `year` and then `artist`
- artists: Stores the information of each unique artists in the music database
  - artist_id as `PRIMARY KEY`, dropped any duplicates from the table as each artist_id is associated with only one artist
- time: timestamps of records in songplays broken down into specific units
  - This allows us to better understand what period of the day/week/month/year do people listen to music
  - start_time as `PRIMARY KEY`, dropped any duplicates from the table as each start_time will have the same date time info
  - Partitioned by `year` and then `month`

## ETL pipeline
- Extract data from input location (S3 bucket)
- Transform song and log data
- Feature engineer additional columns
- Create 1 fact table and 4 dimension tables
- Load the data as partitioned parquet files into output location (S3 bucket)
  - Each table has its own folder within the output location

## Files in the repository
- data: contains log and song data
- dl.cfg: contains AWS key and secret key to access S3 (**remember to DELETE afterwards!**)
- etl.py: extracts data from S3, stages them in Redshift, and transforms data into a set of dimensional tables
- test.ipynb: test code to read/process song/log files and write parquet files using PySpark