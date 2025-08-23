from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests


def print_welcome():
    print('Welcome to Airflow!')


def print_date():
    print('Today is {}'.format(datetime.today().date()))


def print_random_quote():
    # response = requests.get('https://api.quotable.io/random')
    # quote = response.json()['content']
    quote = 'this is a test string quote'
    print('Quote of the day: "{}"'.format(quote))


dag = DAG(
    'welcome_dag',
    default_args={'start_date': datetime(2025, 8, 22)},
    schedule='0 23 * * *',
    catchup=False
)


print_welcome_task = PythonOperator(
    task_id='print_welcome',
    python_callable=print_welcome,
    dag=dag
)


print_date_task = PythonOperator(
    task_id='print_date',
    python_callable=print_date,
    dag=dag
)


print_random_quote = PythonOperator(
    task_id='print_random_quote',
    python_callable=print_random_quote,
    dag=dag
)


# Set the dependencies between the tasks
print_welcome_task >> print_date_task >> print_random_quote