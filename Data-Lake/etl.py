import os
import configparser
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.types import IntegerType, DoubleType, LongType, TimestampType
from pyspark.sql.functions import udf, col, date_format, monotonically_increasing_id
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, dayofweek

# aquire key to access AWS S3
config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['KEY']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['KEY']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    """
    Creates Spark session using PySpark
    """
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    """
    - Get filepath to song data file from input_data location
    - Create song schema and load the song data
    - Create songs_table and load the partitioned parquet data to output_data
    - Create artists_table and load parquet data to output_data location
    """
    # get filepath to song data file
    song_data = f'{input_data}song_data/*/*/*/*.json'
    # song_data = 'data/song_data/*/*/*/*.json' # Test local song data
    
    # create song schema
    song_schema = StructType([
        StructField("artist_id", StringType(), False),
        StructField("artist_latitude", DoubleType(), True),
        StructField("artist_location", StringType(), True),
        StructField("artist_longitude", DoubleType(), True),
        StructField("artist_name", StringType(), False),
        StructField("duration", DoubleType(), False),
        StructField("num_songs", IntegerType(), True),
        StructField("song_id", StringType(), False),
        StructField("title", StringType(), False),
        StructField("year", IntegerType(), True),
    ])
    
    # read song data file (JSON)
    df = spark.read.json(song_data, schema=song_schema)

    # extract columns to create songs table
    songs_table = df.select('song_id', 'title', 'artist_id', 'year', 'duration', 
                            col('artist_id').alias('artist')).drop_duplicates(subset=['song_id'])
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy('year', 'artist').parquet(f'{output_data}songs', mode='overwrite')

    # extract columns to create artists table
    artists_table = df.select('artist_id', 
                              col('artist_name').alias('name'), 
                              col('artist_location').alias('location'), 
                              col('artist_latitude').alias('latitude'), 
                              col('artist_longitude').alias('longitude')) \
                    .drop_duplicates(subset=['artist_id'])
    
    # write artists table to parquet files
    artists_table.write.parquet(f'{output_data}artists', mode='overwrite')


def process_log_data(spark, input_data, output_data):
    """
    - Get file path to log data file from input_data location
    - Load the log data and filter by 'page'='NextSong'
    - Create users_table and load the parquet data to output_data location
    - Feature engineer additional datetime columns
    - Create time_table and load the partitioned parquet data to output_data
    - Create songplays_table by joining tables and load the partitioned 
      parquet data to output_data location
    """
    # get filepath to log data file
    log_data = f'{input_data}log_data/*/*/*.json'
    # log_data = 'data/log_data/*.json' # Test local log data

    # read log data file (JSON)
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.where(df.page=='NextSong')

    # extract columns for users table
    users_table = df.select(col('userId').alias('user_id'),
                            col('firstName').alias('first_name'),
                            col('lastName').alias('last_name'),
                            'gender',
                            'level').drop_duplicates(subset=['user_id'])
    
    # write users table to parquet files
    users_table.write.parquet(f'{output_data}users', mode='overwrite')

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: datetime.fromtimestamp(x/1000.0), TimestampType())
    df = df.withColumn('timestamp', get_timestamp(df.ts))
    
    # extract columns to create time table
    time_table = df.select(col('ts').alias('start_time'), 
                           hour('timestamp').alias('hour'), 
                           dayofmonth('timestamp').alias('day'), 
                           weekofyear('timestamp').alias('week'), 
                           month('timestamp').alias('month'), 
                           year('timestamp').alias('year'), 
                           dayofweek('timestamp').alias('weekday')) \
                 .drop_duplicates(subset=['start_time'])
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy('year','month').parquet(f'{output_data}time', mode='overwrite')

    # read in song data to use for songplays table
    song_df = spark.read.parquet(f'{output_data}songs/*/*/*.parquet')

    # extract columns from joined song and log datasets to create songplays table
    df_joined = (df.alias('a')
                 .join(song_df.alias('b'),
                      (col('a.song') == col('b.title'))&
                      (col('a.length') == col('b.duration')),
                       how='left')
                 .withColumn('songplay_id', monotonically_increasing_id()) # create incrementing unique index
                 .select('songplay_id',
                         col('ts').alias('start_time'),
                         col('userId').alias('user_id'),
                         'level',
                         'song_id',
                         'artist_id',
                         col('sessionId').alias('session_id'),
                         'location',
                         col('userAgent').alias('user_agent'))
                )

    # add year and month columns from time_table
    songplays_table = (df_joined.alias('a')
                       .join(time_table.select(col('start_time').alias('ts'),
                                               'year','month').alias('b'),
                             col('a.start_time')==col('b.ts')).drop('ts'))
    
    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy('year', 'month').parquet(f'{output_data}songplays', mode='overwrite')


def main():
    """
    - Creates Spark session using PySpark
    - Load song and log data from input_data location transform 
      the data and load the parquet files to output location
    """
    spark = create_spark_session()
#     input_data = "data/" # test song data on local
    input_data = "s3a://udacity-dend/"
    output_data = ""
    
    process_song_data(spark, input_data, output_data)
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
