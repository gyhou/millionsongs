import logging
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.postgres_hook import PostgresHook

class DataQualityOperator(BaseOperator):
    """
    Check if table has records and any null values in certain column.
    """
    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 check_list=[],
                 redshift_conn_id="",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.check_list = check_list
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
        redshift = PostgresHook(self.redshift_conn_id)
        
        for table, column in self.check_list:
            records = redshift.get_records(f'SELECT COUNT(*) FROM {table}')
            
            # Check to verify that at least one record was found
            if len(records) < 1 or len(records[0]) < 1:
                logging.error(f"No records present in the destination table '{table}'")
                # Raise an error if less than one record is found
                raise ValueError(f"Data quality check failed. '{table}' returned {records[0][0]} results")
                
            # Check to verify that no null values in selected column
            null_records = redshift.get_records(
                f"SELECT COUNT(*) FROM {table} WHERE {column} IS NULL")
            if len(null_records) > 1 or len(null_records[0]) > 1:
                logging.error(f"Null values present in '{column}' of table '{table}'")
                # Raise an error if null value is found
                raise ValueError(f"Data quality check failed. {column} in {table} returned null values")
                
            logging.info(
                f"Data quality on table '{table}' check passed with {records[0][0]} records, \
                and {null_records} null values on column '{column}'")
            