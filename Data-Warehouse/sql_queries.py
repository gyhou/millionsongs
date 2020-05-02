import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist VARCHAR(MAX),
    auth VARCHAR(100),
    firstName VARCHAR(100),
    gender VARCHAR(10),
    itemInSession INTEGER,
    lastName VARCHAR,
    length FLOAT,
    level VARCHAR(10),
    location VARCHAR(100),
    method VARCHAR(10),
    page VARCHAR(100),
    registration DOUBLE PRECISION,
    sessionId INTEGER,
    song VARCHAR(MAX),
    status INTEGER,
    ts BIGINT,
    userAgent VARCHAR(MAX),
    userId INTEGER
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    artist_id VARCHAR(100),
    artist_latitude FLOAT, 
    artist_location VARCHAR(100), 
    artist_longitude FLOAT,
    artist_name VARCHAR(100), 
    duration FLOAT,
    num_songs INTEGER,
    song_id VARCHAR(100), 
    title VARCHAR(100), 
    year INTEGER
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id BIGINT IDENTITY PRIMARY KEY,
    start_time BIGINT NOT NULL,
    user_id INTEGER NOT NULL,
    level VARCHAR(100) NOT NULL,
    song_id VARCHAR,
    artist_id VARCHAR,
    session_id INTEGER NOT NULL, 
    location VARCHAR NOT NULL, 
    user_agent VARCHAR NOT NULL
);
""")

    
user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY, 
    first_name VARCHAR(100) NOT NULL, 
    last_name VARCHAR(100) NOT NULL, 
    gender VARCHAR(100) NOT NULL, 
    level VARCHAR(100) NOT NULL
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time TIMESTAMP PRIMARY KEY, 
    hour INTEGER NOT NULL, 
    day INTEGER NOT NULL, 
    week INTEGER NOT NULL, 
    month INTEGER NOT NULL, 
    year INTEGER NOT NULL, 
    weekday INTEGER NOT NULL
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR PRIMARY KEY, 
    title VARCHAR NOT NULL, 
    artist_id VARCHAR NOT NULL, 
    year INTEGER, 
    duration FLOAT NOT NULL
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR PRIMARY KEY, 
    name VARCHAR NOT NULL, 
    location VARCHAR,
    latitude FLOAT, 
    longitude FLOAT
);
""")

# STAGING TABLES

staging_events_copy = (f"""
COPY staging_events
FROM {config['S3']['LOG_DATA']}
credentials 'aws_iam_role={config['IAM_ROLE']['ARN']}'
region 'us-west-2' COMPUPDATE OFF
JSON {config['S3']['LOG_JSONPATH']};
""")

staging_songs_copy = (f"""
COPY staging_songs
FROM {config['S3']['SONG_DATA']}
credentials 'aws_iam_role={config['IAM_ROLE']['ARN']}'
region 'us-west-2' COMPUPDATE OFF
JSON 'auto' truncatecolumns;
""")

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays 
(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT events.ts,
       events.userId,
       events.level,
       songs.song_id,
       songs.artist_id,
       events.sessionId,
       events.location,
       events.userAgent
FROM staging_events AS events
LEFT OUTER JOIN staging_songs AS songs
     ON (events.artist = songs.artist_name)
     AND (events.song = songs.title)
     AND (events.length = songs.duration)
     WHERE events.page = 'NextSong';
""")
# 9553 users
user_table_insert = ("""
INSERT INTO users
(user_id, first_name, last_name, gender, level)
SELECT DISTINCT userId, firstName, lastName, gender, level
FROM staging_events
WHERE page = 'NextSong';
""")

time_table_insert = ("""
INSERT INTO time 
(start_time, hour, day, week, month, year, weekday)
SELECT DISTINCT a.start_time,
       EXTRACT (HOUR FROM a.start_time), 
       EXTRACT (DAY FROM a.start_time),
       EXTRACT (WEEK FROM a.start_time), 
       EXTRACT (MONTH FROM a.start_time),
       EXTRACT (YEAR FROM a.start_time), 
       EXTRACT (WEEKDAY FROM a.start_time) 
FROM (SELECT TIMESTAMP 'epoch' + start_time/1000 *INTERVAL '1 second' as start_time 
      FROM songplays) a;
""")

# No duplicates in the data
song_table_insert = ("""
INSERT INTO songs
(song_id, title, artist_id, year, duration)
SELECT distinct song_id, title, artist_id, year, duration
FROM staging_songs;
""")

artist_table_insert = ("""
INSERT INTO artists
(artist_id, name, location, latitude, longitude)
SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude
FROM staging_songs;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
