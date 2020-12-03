from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from core.tension import get_raw, get_avg, calc_avg, compare
from datetime import datetime
from airflow.utils.dates import days_ago


args = {
    'owner': 'Airflow',
    'start_date': datetime.now(),
    'provide_context': True,
    'start_date': days_ago(2),
}

dag = DAG(
    dag_id='TensionAVG',
    default_args=args,
    schedule_interval='*/180 * * * *',
    tags=['seislog'],
    catchup=False
)

get_dates_raw = PythonOperator(task_id='get_dates_raw',
                               python_callable=get_raw,
                               provide_context=True,
                               dag=dag)

get_dates_avg = PythonOperator(task_id='get_dates_avg',
                               python_callable=get_avg,
                               provide_context=True,
                               dag=dag)

compare_dates = BranchPythonOperator(task_id='compare_dates',
                                     provide_context=True,
                                     python_callable=compare,
                                     dag=dag)

calc_avg = PythonOperator(task_id='calc_avg',
                          python_callable=calc_avg,
                          rovide_context=True,
                          dag=dag)

finish = DummyOperator(task_id='finish',
                       dag=dag)

get_dates_raw >> get_dates_avg
get_dates_avg >> compare_dates
compare_dates >> [calc_avg, finish]
calc_avg >> finish