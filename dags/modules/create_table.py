from airflow.providers.postgres.hooks.postgres import PostgresHook

def create_table():
    postgres_hook = PostgresHook(postgres_conn_id='postgres')
    create_table_query = """
        CREATE TABLE IF NOT EXISTS dados_cotacao_btc (
            valor NUMERIC(10, 2) NOT NULL,         -- Numeric value with up to 2 decimal places
            criptomoeda CHAR(6) NOT NULL,          -- Cryptocurrency code 
            moeda CHAR(4) NOT NULL,                -- Currency code
            data_hora TIMESTAMP NOT NULL,          -- Registration date and time
            PRIMARY KEY (criptomoeda, moeda, data_hora) -- Primary key to avoid duplications
        );
    """
    try:
        postgres_hook.run(create_table_query)
        print("Table 'dados_cotacao_btc' created successfully.")
    except Exception as e:
        print(f"Error creating the table: {e}")
        raise