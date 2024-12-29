from pymongo import MongoClient
from dotenv import load_dotenv
import os

#Classe de conexão mongo
class MongoDBHandler:
    def __init__(self, db_name=None, collection_name=None, host=None, port=None):
        load_dotenv()

        self.db_name = str(db_name or os.getenv("MONGO_DB_NAME", "default_db"))
        self.collection_name = str(collection_name or os.getenv("MONGO_DB_COLLECTION", "default_collection"))
        self.host = str(host or os.getenv("DB_HOST", "localhost"))
        self.port = int(port or os.getenv("MONGO_PORT", 27017))

        # Conexão com o MongoDB
        try:
            print(f"Conectando ao MongoDB em {self.host}:{self.port}...")
            self.client = MongoClient(f'mongodb://{self.host}:{self.port}')
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]  # Atribuindo a coleção
            print(f"Conectado ao MongoDB, banco: {self.db_name}, coleção: {self.collection_name}")
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")
            raise


    def insert_one_data(self, document):
        """Insere um único documento na coleção."""
        self.collection.insert_one(document)
        print('Documento inserido: ', document)

    def insert_many_data(self, documents):
        """Insere múltiplos documentos na coleção."""
        self.collection.insert_many(documents)

    def view_data(self):
        """Exibe todos os documentos da coleção."""
        for doc in self.collection.find():
            print(doc)

    def extract_data(self):
        """Retorna todos os documentos da coleção."""
        return self.collection.find()
    

if __name__ == "__main__":
    # Criando uma instância da classe com o banco de dados e coleção desejados
    mongo_handler = MongoDBHandler(db_name='btc_database', collection_name='btc_collection')

    # Inserindo um documento
    mongo_handler.insert_one_data({"amount": 3145678.513, "criptcurrency": "BTC", "currency": "USD"})

    # Inserindo múltiplos documentos
    mongo_handler.insert_many_data([
        {"amount": 3145678.513, "criptcurrency": "BTC", "currency": "USD"},
        {"amount": 4135619.513, "criptcurrency": "BTC", "currency": "USD"}
    ])

    # Visualizando os dados
    mongo_handler.view_data()
    
    # Extraindo os dados
    data = mongo_handler.extract_data()
    for doc in data:
        print(doc)