class SqlQueries:
    # DROP TABLES
    staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
    staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
    songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
    user_table_drop = "DROP TABLE IF EXISTS users;"
    song_table_drop = "DROP TABLE IF EXISTS songs;"
    artist_table_drop = "DROP TABLE IF EXISTS artists;"
    time_table_drop = "DROP TABLE IF EXISTS time;"
    
    # Create Tables
    songplays_table_create = ("""
        CREATE TABLE public.songplays (
            songplay_id bigint IDENTITY NOT NULL,
            start_time timestamp NOT NULL,
            user_id int4 NOT NULL,
            level varchar(256),
            song_id varchar(256),
            artist_id varchar(256),
            session_id int4,
            location varchar(256),
            user_agent varchar(256),
            CONSTRAINT songplays_pkey PRIMARY KEY (songplay_id)
        );""")

    artists_table_create = ("""
        CREATE TABLE public.artists (
            artist_id varchar(256) NOT NULL,
            name varchar(256),
            location varchar(256),
            latitude numeric(18,0),
            longitude numeric(18,0),
            CONSTRAINT artists_pkey PRIMARY KEY (artist_id)
        );""")

    songs_table_create = ("""
        CREATE TABLE public.songs (
            song_id varchar(256) NOT NULL,
            title varchar(256),
            artist_id varchar(256),
            year int4,
            duration numeric(18,0),
            CONSTRAINT songs_pkey PRIMARY KEY (song_id)
        );""")

    users_table_create = ("""
        CREATE TABLE public.users (
            user_id int4 NOT NULL,
            first_name varchar(256),
            last_name varchar(256),
            gender varchar(256),
            level varchar(256),
            CONSTRAINT users_pkey PRIMARY KEY (user_id)
        );""")

    time_table_create = ("""
        CREATE TABLE public.time (
            start_time TIMESTAMP PRIMARY KEY, 
            hour int4 NOT NULL, 
            day int4 NOT NULL, 
            week int4 NOT NULL, 
            month int4 NOT NULL, 
            year int4 NOT NULL, 
            weekday int4 NOT NULL,
            CONSTRAINT time_pkey PRIMARY KEY (start_time)
        );""")

    staging_events_table_create = ("""
        CREATE TABLE public.staging_events (
            artist varchar(256),
            auth varchar(256),
            firstname varchar(256),
            gender varchar(256),
            iteminsession int4,
            lastname varchar(256),
            length numeric(18,0),
            level varchar(256),
            location varchar(256),
            method varchar(256),
            page varchar(256),
            registration numeric(18,0),
            sessionid int4,
            song varchar(256),
            status int4,
            ts int8,
            useragent varchar(256),
            userid int4
        );""")

    staging_songs_table_create = ("""
        CREATE TABLE public.staging_songs (
            num_songs int4,
            artist_id varchar(256),
            artist_name varchar(256),
            artist_latitude numeric(18,0),
            artist_longitude numeric(18,0),
            artist_location varchar(256),
            song_id varchar(256),
            title varchar(256),
            duration numeric(18,0),
            year int4
        );""")

    # Inserting data
    songplay_table_insert = ("""
        INSERT INTO songplays 
        (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
        SELECT
                events.start_time, 
                events.userid, 
                events.level, 
                songs.song_id, 
                songs.artist_id, 
                events.sessionid, 
                events.location, 
                events.useragent
                FROM (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, *
            FROM staging_events
            WHERE page='NextSong') events
            LEFT JOIN staging_songs songs
            ON events.song = songs.title
                AND events.artist = songs.artist_name
                AND events.length = songs.duration
    """)

    user_table_insert = ("""
        INSERT INTO users
        (user_id, first_name, last_name, gender, level)
        SELECT distinct userid, firstname, lastname, gender, level
        FROM staging_events
        WHERE page='NextSong'
    """)

    song_table_insert = ("""
        INSERT INTO songs
        (song_id, title, artist_id, year, duration)
        SELECT distinct song_id, title, artist_id, year, duration
        FROM staging_songs
    """)

    artist_table_insert = ("""
        INSERT INTO artists
        (artist_id, name, location, latitude, longitude)
        SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM staging_songs
    """)

    time_table_insert = ("""
        INSERT INTO time 
        (start_time, hour, day, week, month, year, weekday)
        SELECT start_time, extract(hour from start_time), extract(day from start_time), extract(week from start_time), 
               extract(month from start_time), extract(year from start_time), extract(dayofweek from start_time)
        FROM songplays
    """)
    
    drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
    create_table_queries = [staging_events_table_create, staging_songs_table_create, songplays_table_create, users_table_create, songs_table_create, artists_table_create, time_table_create]