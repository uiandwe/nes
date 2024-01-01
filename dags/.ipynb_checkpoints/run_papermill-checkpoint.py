import redis
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.providers.papermill.operators.papermill import PapermillOperator
from airflow import DAG
from datetime import datetime, timedelta
import airflow.utils.dates
import json
import os



def print_context(ds=None, **kwargs):
    """Print the Airflow context and ds variable from the context."""
    print(kwargs)
    print(ds)
    return "Whatever you return gets printed in the logs"


with DAG(
    dag_id="example_papermill_operator_verify",
    schedule='*/10 * * * *',
    start_date=datetime(2023,12,7),
    catchup=False,
) as dag:
    
    run_bash = BashOperator(
        task_id="run_bash",
        bash_command="echo start dag",
    )
    
    run_example_notebook = PapermillOperator(
        task_id="run_example_notebook",
        input_nb=os.path.join("/opt/airflow/dags/notebook/test_papermill.ipynb"),
        output_nb="/opt/airflow/output/out-{{ execution_date }}.ipynb",
        parameters={
                    "msgs": "Ran from Airflow at {{ execution_date }}!",
                    "execution_date": "{{execution_date}}" 
                   },
    )
    
    done_task = PythonOperator(task_id="done_task", python_callable=print_context)

    run_bash >> run_example_notebook >> done_task