# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS songplay_table;"
user_table_drop = "DROP TABLE IF EXISTS user_table;"
song_table_drop = "DROP TABLE IF EXISTS song_table;"
artist_table_drop = "DROP TABLE IF EXISTS artist_table;"
time_table_drop = "DROP TABLE IF EXISTS time_table;"

# CREATE TABLES
# 1 Fact Table
# songplays - records in log data associated with song plays i.e. records with page NextSong
songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id SERIAL PRIMARY KEY,
    start_time bigint NOT NULL,
    user_id int NOT NULL,
    level varchar NOT NULL,
    song_id varchar,
    artist_id varchar,
    session_id int NOT NULL, 
    location varchar NOT NULL, 
    user_agent varchar NOT NULL
);
""")
# 4 Dimension Tables
# users - users in the app
user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id int PRIMARY KEY, 
    first_name varchar NOT NULL, 
    last_name varchar NOT NULL, 
    gender varchar NOT NULL, 
    level varchar NOT NULL
);
""")
# songs - songs in music database
song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id varchar PRIMARY KEY, 
    title varchar NOT NULL, 
    artist_id varchar NOT NULL, 
    year int, 
    duration decimal NOT NULL
);
""")
# artists - artists in music database
artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id varchar PRIMARY KEY, 
    name varchar NOT NULL, 
    location varchar, 
    latitude decimal, 
    longitude decimal
);
""")
# time - timestamps of records in songplays broken down into specific units
time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time bigint PRIMARY KEY, 
    hour int NOT NULL, 
    day int NOT NULL, 
    week int NOT NULL, 
    month int NOT NULL, 
    year int NOT NULL, 
    weekday int NOT NULL
);
""")

# INSERT RECORDS
# Find the song ID and artist ID based on the title, artist name, and duration of a song.
# Select the timestamp, user ID, level, song ID, artist ID, session ID, location, and user agent and set to songplay_data
songplay_table_insert = ("""
INSERT INTO songplays 
(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO users
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) 
DO UPDATE
    SET first_name = EXCLUDED.first_name, 
    last_name = EXCLUDED.last_name, 
    gender = EXCLUDED.gender, 
    level = EXCLUDED.level
""")

song_table_insert = ("""
INSERT INTO songs
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (song_id) 
DO NOTHING;
""")

artist_table_insert = ("""
INSERT INTO artists
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id) 
DO UPDATE
    SET location = EXCLUDED.location,
    latitude = EXCLUDED.latitude,
    longitude = EXCLUDED.longitude;
""")

time_table_insert = ("""
INSERT INTO time
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time) 
DO NOTHING;
""")

# FIND SONGS

song_select = ("""
SELECT s.song_id, a.artist_id
FROM songs s join artists a ON s.artist_id=a.artist_id
WHERE s.title = %s AND a.name = %s AND s.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]