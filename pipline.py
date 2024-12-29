import requests
import time
from datetime import datetime
from mongo_conn import MongoDBHandler



#Extract
def extract_btc_data():
    url = 'https://api.coinbase.com/v2/prices/spot'
    response = requests.get(url)
    return response.json()['data']

     
#Transform
def transform_btc_data(json_data):
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

def load_btc_data(data):
    print(data)
    mongodb = MongoDBHandler()
    
    if not data:
        print('Dados vazio, nada a inserir.')
        return
    
    try:
        if isinstance(data, list) and len(data) > 1:
            mongodb.insert_many_data(data)
        else:
            mongodb.insert_one_data(data)
    except Exception as e:
        print(f'Ocorreu um erro ao tentar carregar os dados: {e}')



if __name__ == '__main__':
    while True:
        #Extract
        json_data = extract_btc_data()
        #Transform 
        processed_data = transform_btc_data(json_data)
        #Load
        load_btc_data(processed_data)
        time.sleep(15)
