import logging
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.postgres_hook import PostgresHook


class LoadFactOperator(BaseOperator):
    """
    Load fact table, only allow append functionally when inserting data.
    """
    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 table="",
                 sql_query="",
                 redshift_conn_id="",
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.sql_query = sql_query
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
        redshift = PostgresHook(self.redshift_conn_id) 
        logging.info(f"Inserting data from staging table data to {self.table}")
        redshift.run(self.sql_query)
        