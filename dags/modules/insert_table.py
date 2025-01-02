from airflow.providers.postgres.hooks.postgres import PostgresHook

def insert_data(transformed_data):
    postgres_hook = PostgresHook(postgres_conn_id='postgres')

    insert_data_query = """INSERT INTO dados_cotacao_btc(valor, criptomoeda, moeda, data_hora)
                            VALUES (%s, %s, %s, %s)"""

    
    postgres_hook.run(insert_data_query, parameters=(
        transformed_data['valor'],
        transformed_data['criptomoeda'],
        transformed_data['moeda'],
        transformed_data['data_hora']
    ), autocommit=True)

    print("Data loaded into the database successfully:", transformed_data)