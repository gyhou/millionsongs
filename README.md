# Data Engineering with Millionsongs subset data
## Project Datasets
### Song Dataset
**S3 Song Data Source** - s3://udacity-dend/song_data
- Subset of the real data from [Million Song Dataset](http://millionsongdataset.com/)
- Each file is in JSON format and contains metadata about a song and the artist of that song

### Log Dataset
**S3 Log Data Source** - s3://udacity-dend/log_data
- Log files are in JSON format generated by this [event simulator](https://github.com/Interana/eventsim) based on the songs in the dataset above
- These simulate activity logs from a music streaming app based on specified configurations
- The dataset are partitioned by year and month

## Database schema design
We have 1 fact table (songplays), and 4 dimension tables (users, songs, artists, time).
![](Song_ERD.png)

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
  
## Data Modeling with PostgreSQL
- Used postgres to create database schema and perform data pipeline ETL

## Data Warehouse (AWS Redshift, S3)
- Performs ETL loading data from S3 to Redshift

## Data Lake (Spark, AWS Redshift, S3)
- Performs ETL loading data from S3 using Spark to Redshift

## Data Pipeline with Airflow
