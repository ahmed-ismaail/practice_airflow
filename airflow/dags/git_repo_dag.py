from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.github.operators.github import GithubOperator
from airflow.operators.empty import EmptyOperator as DummyOperator
import logging

# Define the DAG
dag = DAG(
    'git_repo_dag',
    default_args={'start_date': datetime(2025, 8, 24)},
    schedule='0 21 * * *',
    catchup=False
)

# Start Dummy Operator
start = DummyOperator(task_id='start', dag=dag)

# List Git Repository Tags
list_repo_tags = GithubOperator(
    task_id="list_repo_tags",
    github_method="get_repo",
    github_method_args={"full_name_or_id": "hoppscotch/hoppscotch"},
    result_processor=lambda repo: logging.info(list(repo.get_tags())),
    dag=dag,
)

# End Dummy Operator
end = DummyOperator(task_id='end', dag=dag)

# Define task dependencies
start >> list_repo_tags >> end