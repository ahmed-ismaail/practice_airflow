# Imports
from airflow import DAG
from datetime import datetime
from airflow.operators.email import EmailOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator  # Use generic SQL operator

# Define the DAG
dag = DAG(
    'postgresql_orders_dag',
    default_args={'start_date': datetime(2025, 8, 24)},
    schedule='0 21 * * *',
    catchup=False
)

# Define the Task
# get_orders contains the result of the SQL query to retrieve orders
get_orders = SQLExecuteQueryOperator(
    task_id='get_orders',
    sql='./sqls/orders.sql',
    conn_id='postgres_conn2',
    autocommit=False,  # optional
    return_last=True,  # <-- Needed to send result to XCom
    dag=dag
)

send_email = EmailOperator(
    task_id='send_email',
    to="{{ var.value.get('email') }}",
    subject='orders table load - Successful',
    html_content="{{ task_instance.xcom_pull(task_ids='get_orders') }}", # what does this do? this pulls the result of the get_orders task
    dag=dag,
)


# Define the Dependencies
get_orders >> send_email