import logging
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.hooks.postgres_hook import PostgresHook


class CreateTablesOperator(BaseOperator):

    ui_color = '#4CAF50'
    
    @apply_defaults
    def __init__(self,
                 drop_table_queries="",
                 create_table_queries="",
                 redshift_conn_id="",
                 *args, **kwargs):

        super(CreateTablesOperator, self).__init__(*args, **kwargs)
        self.drop_table_queries = drop_table_queries
        self.create_table_queries = create_table_queries
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
#         self.log.info('DataQualityOperator not implemented yet')
        redshift = PostgresHook(self.redshift_conn_id)
        
        for index, query in enumerate(self.drop_table_queries):
            logging.info(f"Dropping table {index+1}")
            redshift.run(query)

        for index, query in enumerate(self.create_table_queries):
            logging.info(f"Creating table {index+1}")
            redshift.run(query)
