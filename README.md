# Data Engineering with Millionsongs subset data
**Original Source** - http://millionsongdataset.com/

**Song Data Source** - s3://udacity-dend/song_data

**Meta Log Data Source** - s3://udacity-dend/log_data

## Database schema design
We have 1 fact table (songplays), and 4 dimension tables (users, songs, artists, time).
![](Song_ERD.png)

## Data Modeling with PostgreSQL
- Used postgres to create database schema and perform data pipeline ETL

## Data Warehouse (AWS Redshift, S3)
- Performs ETL loading data from S3 to Redshift

## Data Lake (Spark, AWS Redshift, S3)
- Performs ETL loading data from S3 using Spark to Redshift

## Data Pipeline with Airflow
