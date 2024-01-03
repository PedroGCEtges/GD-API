from pymongo import MongoClient
from config import MONGO_URL
from datetime import datetime, timedelta

client = MongoClient(MONGO_URL)

def user_collection():
    db = client["Users"]
    users = db["users"]
    return users

def gd_database():
    db = client["GD"]
    return db

def gd_station_collection(name_station : str):
    db = gd_database()
    station = db[name_station]
    return station

def gd_command_history():
    db = gd_database()
    station = db["Command"]
    return station

def get_tags_interval_date(start, end, collection):
    filter = {"timestamp": {"$gte": start, "$lte": end}}
    cursor = collection.find(filter)
    documents = []
    
    for document in cursor:
        documents.append(document)
        print(document)
    return documents
# users.delete_one({"full_name": "admin"})

def get_station_status(collection):
    result = collection.aggregate([
        {"$sort": {"timestamp": -1}}, # Ordenar os documentos pelo timestamp em ordem decrescente
        {"$limit": 1}, # Limitar o número de documentos retornados para apenas um
        {"$project": {"tags": 1}}, # Retornar apenas o campo tags do documento selecionado
        {"$project": {"tags": {"$filter": {"input": "$tags", "as": "tag", "cond": {"$eq": ["$$tag.name", "M_STATUS"]}}}}}, # Filtrar a lista de tags pelo nome da tag desejada
        {"$project": {"value": {"$first": "$tags.value"}}}
    ])

    if result["value"] == 0:
        return "Estação parada"
    
    else:
        return "Estação operando"
    

def get_station_working_status_interval(start, end, station):
    stat = gd_station_collection(station)

    inicio = parse_string_to_datetime(start)
    fim = parse_string_to_datetime(end)

    query = {"timestamp": {"$gte": inicio, "$lt": fim}}
    resultados = stat.find(query).sort("timestamp")
   
    tempo_total = timedelta()
    valor_anterior = None
    tempo_anterior = None

    for doc in resultados:
        tempo = doc["timestamp"]
        valor = doc["tags"]
        for tag in valor:
            if tag["name"] == "M_STATUS":
                value = tag["value"]
        if valor_anterior == 0 and value == 1:
            diferenca = tempo - tempo_anterior
            tempo_total += diferenca
        valor_anterior = value
        tempo_anterior = tempo
    print(f"O tempo total que a tag M_STATUS teve o valor 1 foi de {tempo_total}")
    return tempo_total


def parse_string_to_datetime(date):
    if isinstance(date, str):
        formato = "%Y-%m-%dT%H:%M:%S.%fZ"
        new_date = datetime.strptime(date, "%d/%m/%Y")
    return new_date

def query_time_and_value_in_mongo(db="Teste", collection="teste",start=datetime(2023, 12, 5, 0, 0, 0), end=datetime(2023, 12, 6, 0, 0, 0) ):
    mongo_db = client[db]
    mongo_col = mongo_db[collection] 

    pipeline = [
        {'$match': {'timestamp': {'$gte': start, '$lte': end}}},
        {'$unwind': '$tags'},
        {'$group': {
            '_id': '$tags.name',
            "timestamp": {"$push": "$$ROOT.tags.timestamp"},
            "value":{"$push": "$$ROOT.tags.value"}
        }},
        {'$project': {
            '_id': 0,
            'tag': '$_id',
            "timestamp": 1,
            "value": 1,
        }}
    ]

    resultado = mongo_col.aggregate(pipeline)
    return resultado


def create_dict_with_tupled_values(resultado):
    aux_dict = {}

    for doc in resultado:
        teste = []
        for i in range(len(doc["timestamp"])):
            teste.append((doc["timestamp"][i],doc["value"][i]))
        aux_dict[doc["tag"]] = teste
    return aux_dict


def get_time_diff(aux_dict):
    final_dict = {}
    for key, value in aux_dict.items():
        tempo_total = timedelta()
        valor_anterior = None
        tempo_anterior = None
        for v in range(len(value)):
            intervalo_de_operacao = datetime.strptime(value[-1][0],"%Y-%m-%dT%H:%M:%S.%f") - datetime.strptime(value[0][0],"%Y-%m-%dT%H:%M:%S.%f") 

            if valor_anterior == None:
                valor_anterior = value[v][1]
            if tempo_anterior == None:
                tempo_anterior = datetime.strptime(value[v][0],"%Y-%m-%dT%H:%M:%S.%f")

            if value[v][1] != valor_anterior:  
                if value[v][1] == 1:
                    diff = datetime.strptime(value[v][0],"%Y-%m-%dT%H:%M:%S.%f") - tempo_anterior
                    tempo_total += diff

            valor_anterior = value[v][1]
            tempo_anterior = datetime.strptime(value[v][0],"%Y-%m-%dT%H:%M:%S.%f")

        if intervalo_de_operacao.total_seconds() !=0:
            final_dict[key] =  { "Tempos": {
                        "Tempo de Operação": f'{intervalo_de_operacao}',
                        "Tempo trabalhando": f'{tempo_total}',
                        "Tempo Ocioso": f'{intervalo_de_operacao - tempo_total}',
                        },
                        "Relativos" : {
                            "Tempo de Operação": f'{tempo_total/intervalo_de_operacao}',
                            "Tempo Ocioso": f'{(intervalo_de_operacao - tempo_total)/intervalo_de_operacao}'
                        }
                        }
        else:
            final_dict[key] = "Sem dados de operação"
    return final_dict