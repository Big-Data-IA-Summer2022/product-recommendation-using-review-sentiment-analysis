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
    dag_id='bestsellerdag',
    schedule_interval=None,
    start_date=pendulum.datetime(2022, 7, 22, tz="UTC"),
    catchup=False
) as dag:
    t1 = BashOperator( task_id='Scraping_bestseller_products', bash_command='cd /opt/airflow/dags; python ScrapingAmazonReviews.py')
    t2 = BashOperator( task_id='scraping_reviews_and_update_ratings_for_every_category', bash_command='cd /opt/airflow/dags; python bestsellerratingsupdate.py')


t1>>t2