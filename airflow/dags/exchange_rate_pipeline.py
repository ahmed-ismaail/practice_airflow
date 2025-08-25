import sys
import os 
# regardless of the current working directory from which the script is run get the absolute path of the parent directory 
# to ensure the plugins directory is included in the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 
print("sys.path:", sys.path)
print("plugins exists:", os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'plugins')))

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from plugins.clean_data import clean_data

dag = DAG(
    'exchange_rate_etl', # DAG name
    description='A simple ETL pipeline to download, clean, and email exchange rate data',
    start_date=datetime(2025, 8, 24),
    end_date=datetime(2025, 12, 31),
    schedule='0 22 * * *',
    default_args={"retries": 2, "retry_delay": timedelta(minutes=5)}, # Retry twice with a 5-minute delay
    catchup=False # Do not perform backfill runs
)

#operators
#they are the building blocks of a workflow to perform a specific task
# they are defined as instances of operator classes

# Define or Instantiate Tasks
download_task = BashOperator(
    task_id='download_file', # Task name
    # this command curl stands for "Client URL" and is used to transfer data from or to a server
    # the -o option is used to specify the output file name
    # the URL is the location of the file to be downloaded
    bash_command="curl -o xrate.csv '{{ var.value.get('rate_api_url')}}'", # Command to download the file
    cwd='/tmp', # cwd stand for "current working directory" to Change to /tmp directory before executing the command
    dag=dag, # Associate this task with the DAG defined above
)

clean_data_task = PythonOperator(
    task_id='clean_data', # Task name
    python_callable=clean_data, # Function to be called
    do_xcom_push=False,  # prevent any return value serialization
    dag=dag, # Associate this task with the DAG defined above
)

send_email_task = EmailOperator(
    task_id='send_email', # Task name
    to="{{ var.value.get('email') }}", # Recipient email address
    subject='Exchange Rate Download - Successful', # Email subject
    html_content='The Exchange Rate data has been successfully downloaded, cleaned, and loaded.', # Email body content
    dag=dag,
)

# Define Task Dependencies
download_task >> clean_data_task >> send_email_task