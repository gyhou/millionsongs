import os
from airflow import DAG
from helpers import SqlQueries
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator, 
                               LoadDimensionOperator, DataQualityOperator)

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

"""
1. Run "/opt/airflow/start.sh" command to start Airflow web server
2. Set up AWS Credential and Redshift database on Airflow's admin/connections
3. Create tables through Redshift query editor first (SQL queries in create_tables.sql)
4. Toggle DAG on in Airflow web server when ready

- Please note: Because the files located in the s3 bucket 'udacity-dend' are very large, 
Airflow can take up to 10 minutes to make the connection.
"""

default_args = {
    'owner': 'udacity',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email': ['test@email.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    # Catchup in DAG
}

dag = DAG('sparkify-dag',
          catchup=False,
          default_args=default_args,
          schedule_interval='@hourly',
          description='Load and transform data in Redshift with Airflow',
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

# stages log data from S3 to Redshift
stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    table="staging_events",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udacity-dend",
    s3_key="log_data",
    s3_region ="us-west-2",
    json_path="s3://udacity-dend/log_json_path.json",
)

# stages song data from S3 to Redshift
stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    table="staging_songs",
    redshift_conn_id="redshift",
    aws_credentials_id="aws_credentials",
    s3_bucket="udacity-dend",
    s3_key="song_data",
    s3_region ="us-west-2",
    json_path="auto",
)

# Load data to songplays table
# Fact tables are usually so massive so only allow append type functionality
load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    table='songplays',
    redshift_conn_id="redshift",
    sql_query = SqlQueries.songplay_table_insert,
)

# Load data to users table
load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    table='users',
    delete_or_append='delete',
    redshift_conn_id="redshift",
    sql_query = SqlQueries.user_table_insert,
)

# Load data to songs table
load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    table='songs',
    delete_or_append='delete',
    redshift_conn_id="redshift",
    sql_query = SqlQueries.song_table_insert,
)

# Load data to artists table
load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    table='artists',
    delete_or_append='delete',
    redshift_conn_id="redshift",
    sql_query = SqlQueries.artist_table_insert,
)

# Load data to time table
load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    table='time',
    delete_or_append='delete',
    redshift_conn_id="redshift",
    sql_query = SqlQueries.time_table_insert,
)

# Check if data quality in all 5 tables
run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    # Check data quality in (table name, column in table)
    check_list=[('songplays', 'songplay_id'),
                ('users', 'user_id'),
                ('songs', 'song_id'),
                ('artists', 'artist_id'),
                ('time', 'start_time')],
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


start_operator >> [stage_songs_to_redshift, stage_events_to_redshift] >> load_songplays_table
load_songplays_table >> [load_song_dimension_table, load_artist_dimension_table, load_user_dimension_table, load_time_dimension_table] >> run_quality_checks
run_quality_checks >> end_operator
