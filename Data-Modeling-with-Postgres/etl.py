import os
import glob
import psycopg2
import numpy as np
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    - Open song file
    - Insert song record to the songs table
    - Insert artist record to the artists table
    """
    # open song file
    df = pd.read_json(filepath, lines=True)
    
    # Replace none values with proper Null values
    df['artist_location'].replace('', np.nan, inplace=True)
    df['year'].replace(0, np.nan, inplace=True)
    
    # insert song record
    song_data = df[['song_id','title','artist_id','year','duration']].values[0]
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    - Open log file
    - Filter data to only show NextSong pages
    - Feature engineer additional datetime columns
    - Insert time data into time table
    - Load and insert user details to users table
    - Combine data from multiple tables to insert into songplay table
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = list(zip(list(df['ts']), list(t.dt.hour), 
                         list(t.dt.day), list(t.dt.week), 
                         list(t.dt.month), list(t.dt.year), 
                         list(t.dt.weekday)))
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(time_data, columns=column_labels, dtype=int)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    - Get all files matching extension from directory
    - Get total number of files found
    - Iterate over files and process
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - Establishes connection with the sparkify database and gets cursor to it.
    - Process song data
    - Process log data
    - Finally, closes the connection.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()