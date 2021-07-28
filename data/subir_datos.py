import random
from random import randint
from pymongo import MongoClient
import datetime

MONGO_URI = 'mongodb://localhost'

client = MongoClient(MONGO_URI)

db = client['FlyBot']

def upload_data():
    #Intanciacion de atributos fecha salida y fecha llegada
    numero_de_vuelo = 1
    inicio = datetime.date(2020, 10, 10)
    final = datetime.date(2020, 12, 31)
    #Creacion de la coleccion Vuelos y asignacion a la variable
    vuelos_collection = db['vuelos']
    #Lectura del archivo vuelos.txt
    file = open("vuelos.txt", "r", encoding='utf8')
    #Asignacion a la var lines de lo que habia en el archivo .txt
    lines = file.readlines()
    it = 0
    for i in range(50):
        random_date_ida = inicio + (final - inicio) * random.random()
        random_date_llegada = inicio + (final - inicio) * random.random()
        ida = lines[randint(0, len(lines) - 1)].split(",")
        llegada = lines[randint(0, len(lines) - 1)].split(",")
        if ida[1] != llegada[1]:
            if it % 2 == 0:
                it += 1
                if random_date_llegada > random_date_ida:
                    vuelos_collection.insert_one(
                        {
                            "numero de vuelo": numero_de_vuelo,
                            "origen": {
                                "ciudad": ida[0],
                                "IATA": ida[1],
                                "provincia": ida[2],
                                "pais": ida[3][:-1]
                            },
                            "destino": {
                                "ciudad": llegada[0],
                                "IATA": llegada[1],
                                "provincia": llegada[2],
                                "pais": llegada[3][:-1]
                            },
                            "fecha de ida": str(random_date_ida),
                            "fecha de llegada": str(random_date_llegada)
                        }
                    )
                    numero_de_vuelo += 1
            else:
                it += 1
                vuelos_collection.insert_one(
                    {
                        "numero de vuelo": numero_de_vuelo,
                        "origen": {
                            "ciudad": ida[0],
                            "IATA": ida[1],
                            "provincia": ida[2],
                            "pais": ida[3][:-1]
                        },
                        "destino": {
                            "ciudad": llegada[0],
                            "IATA": llegada[1],
                            "provincia": llegada[2],
                            "pais": llegada[3][:-1]
                        },
                        "fecha de ida": str(random_date_ida),
                        "fecha de llegada": ""
                    }
                )
                numero_de_vuelo += 1

upload_data()