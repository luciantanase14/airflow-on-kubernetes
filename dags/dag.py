from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='kubernetes_executor_test_dag',
    default_args=default_args,
    description='To test the DAG to validate KubernetesExecutor setup with Airflow',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 9, 14),
    catchup=False,
    tags=['test', 'kubernetes', 'airflow'],
) as dag:

    print_date = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    run_kubernetes_pod = KubernetesPodOperator(
        task_id='run_kubernetes_pod',
        name='test-pod',
        namespace='default',
        image='busybox:latest',
        cmds=['echo', 'Kubernetes Executor Test Successful!'],
        get_logs=True,
    )

    print_date >> run_kubernetes_pod
