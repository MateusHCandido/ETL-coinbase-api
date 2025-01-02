from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime
from datetime import timedelta

from modules.create_table import create_table
from modules.insert_table import insert_data


dag = DAG('extract_data_coinbase_api', #DAG name
          'extraction of data by Coinbase API', #Description
          start_date=datetime(2024, 12, 29),
          schedule_interval=timedelta(seconds=15),  
          catchup=False) #Avoid retroactive execution

     
## FUNCTIONS ##

def transform_btc_data(ti):
    json_data = ti.xcom_pull(task_ids='extract_btc_data')
    if json_data:
        valor = json_data['amount']
        criptomoeda = json_data['base']
        moeda = json_data['currency']

        transformed_value = {
            'valor': valor,
            'criptomoeda': criptomoeda,
            'moeda': moeda,
            'data_hora': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return transformed_value
    raise ValueError('Not found data in xcom for "extract_btc_data" method.')

def load_btc_data(ti):
    data = ti.xcom_pull(task_ids='transform_btc_data')
    if not data:
         raise ValueError('Not found data in xcom for "load_btc_data" method.')
    else:
        try:
            create_table()
            insert_data(data)
        except Exception as e:
            print(f'An error occurred when trying to load the data:: {e}')


## TASK ##


extract_btc_data_task = SimpleHttpOperator(
    task_id='extract_btc_data',
    http_conn_id='coinbase_api', #Connection configured in airflow
    endpoint='v2/prices/spot',
    method='GET',
    response_filter=lambda response: response.json()['data'],
    log_response=True,
    dag=dag
    )

transform_btc_data_task = PythonOperator(
    task_id='transform_btc_data',
    python_callable=transform_btc_data,
    provide_context=True,
    dag=dag
)

load_btc_data_task = PythonOperator(
    task_id='load_btc_data',
    python_callable=load_btc_data,
    dag=dag
)



extract_btc_data_task >> transform_btc_data_task >> load_btc_data_task