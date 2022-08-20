from airflow import DAG
from airflow.operators.bash import BashOperator
import pendulum
from airflow.decorators import task
from airflow.operators.docker_operator import DockerOperator



default_args = {
    'owner': 'airflow',
    'concurrency': 1,
    'retries': 0,
    'depends_on_past': False
}

with DAG(
    dag_id='review_rating_using_asin',
    schedule_interval=None,
    start_date=pendulum.datetime(2022, 7, 22, tz="UTC"),
    catchup=False
) as dag:
    t1 = BashOperator( task_id='generating_reviews_using_asin', bash_command='cd /opt/airflow/dags; python scraperforasin.py')



t1