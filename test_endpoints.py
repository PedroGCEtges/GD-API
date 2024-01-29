# from fastapi.security import OAuth2PasswordRequestForm
from controllers.gd_controller import stop_station
from controllers.user_controller import create_user, delete_user, login
import asyncio
from database.mongodb import gd_station_collection
from models.station import Station
from security import get_current_user
import requests
from models.user import User
from security import is_admin
import random
import datetime

# variables
# atr = {"username": "admin", "password": "secret"}
atr1 = {"username": "User2", "password": "senha"}
user1 = {"username": "User2", "email": "test11124111e@ts.ce","role": "admin"}
# # user1 = {"username": "User2", "email": "test1q1111e@ts.ce","role": "operator" }


# Direct funciton test

# test_user = User(**user1)


# user = OAuth2PasswordRequestForm(**atr1)
# teste = asyncio.run(login(user))
# print(teste['access_token'])

# test = asyncio.run(delete_user(User(**user1),asyncio.run(get_current_user(teste['access_token']))))
# print(test)

# API calls tests

# r = requests.get('http://127.0.0.1:8000/gd/getAllStatus')
# print(r)
r1 = requests.post('https://gd-api-liard.vercel.app/users/login', data=atr1)
token = r1.json()["access_token"]

headers = {"Authorization": f"Bearer {token}"}
password = {'password':'senha'}

print(r1.text)


# Criar uma lista vazia para armazenar os dicionários
lista = []

# Gerar um número aleatório entre 1 e 10 para o tamanho da lista
n = random.randint(1, 10)

# Criar um loop para gerar os dicionários e adicioná-los à lista
for i in range(n):
    # Gerar valores aleatórios para as chaves do dicionário
    name = random.choice(["M_STOP", "M_START", "M_RESET"])
    datetime_var = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tipo = random.choice(["int","bool"])
    if tipo == "int":
        value = random.randint(0, 100)
    else:
        if name == 'M_STOP':
            value = False
        value = bool(random.getrandbits(1))
    # Criar um dicionário com as chaves e valores gerados
    dicionario = {"name": name, "id": id, "datetime": datetime_var, "tipo": tipo, "value": value}

    # Adicionar o dicionário à lista
    lista.append(dicionario)

# Imprimir a lista de dicionários
tags = lista
atr = {"name": "Distributing",
       "id":1,
       "tags": tags,
       "datetime": datetime.datetime.now()}


station = Station(**atr)
teste_1 = gd_station_collection("Distributing")
teste_1.insert_one(station.model_dump())
ultimo_documento = teste_1.find_one(sort=[('datetime', -1)])

# station = Station(**atr)
# teste_1 = gd_station_collection("Distributing")
# teste_1.insert_one(station.model_dump())

# ultimo_documento = teste_1.find_one(sort=[('datetime', -1)])


# # print(ultimo_documento)
# station = {"name": "Distributing"}

# print(asyncio.run(stop_station(station["name"],asyncio.run(get_current_user(teste['access_token'])))))
# r = requests.post(f'https://gd-api-liard.vercel.app/gd/stop_station',  params='station=Distributing', headers=headers)
r = requests.get(f'https://gd-api-liard.vercel.app/gd/getStatus',  params='station=Distributing')
print(r.content)

# # print(asyncio.run(stop_station(station["name"],asyncio.run(get_current_user(teste['access_token'])))))
# r = requests.post(f'http://127.0.0.1:8000/gd/stop_station',  params='station=Distributing', headers=headers)
# print(r.content)
