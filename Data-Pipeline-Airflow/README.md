# Data Pipeline with Airflow
- Built a dynamic and reusable ETL pipeline through data quality checks
- All the tasks have a dependency and DAG begins with a start_execution task and ends with a end_execution task.

## Dag configuration
### DAG contains default_args dict, with the following keys:
- Owner
- Depends_on_past
- Start_date
- Retries
- Retry_delay
- Catchup

- DAG can be scheduled to run once an hour

## Staging the data
### Stages data from S3 to Redshift
- Data is loaded to the staging tables in Redshift using `COPY` statement

### Uses params to generate the copy statement dynamically
- Dynamically generated copy statements as opposed to static SQL statements

### Operator contains logging in different steps of the execution
- `logging.info` shows the progress of staging load

### SQL statements are executed using a Airflow hook
- Connected to the Redshift database via an Airflow hook

## Loading dimensions and fact table
### Dimensions are loaded with on the LoadDimension operator
- Separated functional operator for dimensions (`LoadDimensionOperator`)

### Facts are loaded with on the LoadFact operator
- Separated functional operator for facts (`LoadFactOperator`)

### Task uses params to generate the copy statement dynamically
- Dynamically generated copy statements as opposed to static SQL statements

### DAG allows to switch between append-only and delete-load functionality

## Data Quality Checks
- Data quality check is done with correct operator
- Set up DAG to either fail or retries 3 times
- Operator uses params to get the tests and the results, tests are not hard coded to the operator
