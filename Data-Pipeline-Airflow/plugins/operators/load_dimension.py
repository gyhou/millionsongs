import logging
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.postgres_hook import PostgresHook


class LoadDimensionOperator(BaseOperator):
    """
    Load dimension table, choose between append or delete 
    functionally when inserting data.
    """
    ui_color = '#80BD9E'

    @apply_defaults
    def __init__(self,
                 table="",
                 sql_query="",
                 redshift_conn_id="",
                 delete_or_append="",
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.sql_query = sql_query
        self.delete_or_append = delete_or_append
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
        redshift = PostgresHook(self.redshift_conn_id)
        
        if self.delete_or_append.lower() == 'delete':
            logging.info(f"Deleting data from {self.table}")
            redshift.run(f"DELETE FROM {self.table}")
            
        logging.info(f"Inserting to {self.table}")
        redshift.run(self.sql_query)
