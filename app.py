#pylint disable=C0114
from pymongo import MongoClient
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from exception import ConnectionException
class FlyBot():
    """ Clase Bot """

    MONGO_URI ='mongodb://localhost'
    TELEGRAM_TOKEN = '1297174030:AAHL3kJ-spL63Lr4VTAbcu7pZ3SniKdSvuA'
    DATABASE_NAME = "FlyBot"
    @classmethod
    def __init__(cls):
        cls.connect()
        cls.create_db(cls.DATABASE_NAME)
        cls.metodos()

    @classmethod
    def connect(cls):
        """ Conectar a BD """
        try:
            cls.client = MongoClient(cls.MONGO_URI)
            print("Conexión a MongoDB exitosa.")
        except ConnectionException as err:
            print(f'Ha ocurrido un error durante la conexión a MongoDB {err}')

    @classmethod
    def create_db(cls, db_name):

        """ Creacion de conexion """
        try:
            cls.db = cls.client[db_name]
            print(f"Usando {db_name}.")
        except ConnectionException as err:
            print('Ha ocurrido un error durante la'
            +f' conexión o creación de la base de datos - {err}')

    @classmethod
    def start(cls, update):
        """ Empieza el Bot """
        update.message.reply_text('Hola, los comandos a usar son los siguientes:' +
                                  '\n/start -> Muestra todos los comandos.' +
                                  '\n/list -> Lista todos los vuelos disponibles.' +
                                  '\n/searchd (destino) -> Busca los vuelos disponibles con el destino indicado.' +
                                  '\n/searcho (origen) -> Busca los vuelos disponibles con el origen indicado.' +
                                  '\n/buyticket (nombre) (apellido) (cedula) (número de asientos) (número de vuelo) -> Reserva vuelos sin fecha de retorno.' +
                                  '\n/buyrtticket (nombre) (apellido) (cedula) (número de asientos) (número de vuelo) -> Reserva vuelos con fecha de retorno.')

    @classmethod
    def list(cls, update):
        """ Comando lista de vuelos """
        try:
            cls.vuelos_collection = cls.db['vuelos']
            vuelos = cls.vuelos_collection.find()
            for vuelo in vuelos:
                update.message.reply_text(
                    "\n\nDestino: {}, {}, {}, {}".format(
                        *vuelo['destino'].values()) + "\nOrigen: {}, {}, {}, {}".format(
                        *vuelo['origen'].values()) + "\nFecha de ida: {}".format(
                        vuelo["fecha de ida"]) + "\nFecha de llegada: {}".format(
                        vuelo["fecha de llegada"]) + "\nNúmero de vuelo: {}".format(
                            vuelo['numero de vuelo'])
                )
        except ConnectionException as err:
            print(err)
            update.message.reply_text('Algo ha ocurrido mal.')

    @classmethod
    def searchd(cls, update):
        """ Busca todos los vuelos destino"""
        argumento = " ".join(update.message['text'].split(" ")[1:])
        try:
            cls.vuelos_collection = cls.db['vuelos']
            vuelos = cls.vuelos_collection.find({'$or': [
                {'destino.ciudad': argumento},
                {'destino.IATA': argumento},
                {'destino.pais': argumento},
                {'destino.provincia': argumento}
            ]})
            for vuelo in vuelos:
                update.message.reply_text(
                    "\n\nDestino: {}, {}, {}, {}".format(
                        *vuelo['destino'].values()) + "\nOrigen: {}, {}, {}, {}".format(
                        *vuelo['origen'].values()) + "\nFecha de ida: {}".format(
                        vuelo["fecha de ida"]) + "\nFecha de llegada: {}".format(
                        vuelo["fecha de llegada"]) + "\nNúmero de vuelo: {}".format(
                            vuelo['numero de vuelo'])
                )
        except ConnectionException as err:
            print(err)
            update.message.reply_text('Algo ha ocurrido mal.')

    @classmethod
    def searcho(cls, update):
        """ Busca los vuelos origen """
        argumento = " ".join(update.message['text'].split(" ")[1:])
        try:
            cls.vuelos_collection = cls.db['vuelos']
            vuelos = cls.vuelos_collection.find({'$or': [
                {'origen.ciudad': argumento},
                {'origen.IATA': argumento},
                {'origen.pais': argumento},
                {'origen.provincia': argumento}
            ]})
            for vuelo in vuelos:
                update.message.reply_text(
                    "\n\nDestino: {}, {}, {}, {}".format(
                        *vuelo['destino'].values()) + "\nOrigen: {}, {}, {}, {}".format(
                        *vuelo['origen'].values()) + "\nFecha de ida: {}".format(
                        vuelo["fecha de ida"]) + "\nFecha de llegada: {}".format(
                        vuelo["fecha de llegada"]) + "\nNúmero de vuelo: {}".format(
                            vuelo['numero de vuelo'])
                )
        except ConnectionException as err:
            print(err)
            update.message.reply_text("Algo ha ocurrido mal.")

    @classmethod
    def buyticket(cls, update):
        """ Comprar vuelo """
        argumentos = update.message['text'].split(" ")[1:]
        if len(argumentos) != 5:
            update.message.reply_text('Debe completar los campos requeridos.')
            return
        try:
            cls.vuelos_collection = cls.db['vuelos']
            cls.usuarios_collection = cls.db['usuarios']
            vuelo = cls.vuelos_collection.find_one(
                {'numero de vuelo': int(argumentos[4])})
            if vuelo['fecha de llegada'] != '':
                update.message.reply_text(
                    'Con este comando solo puede reservar un vuelo sin fecha de retorno.')
                return
            cls.usuarios_collection.insert_one({
                "nombre": argumentos[0],
                "apellido": argumentos[1],
                "cedula": argumentos[2],
                "numero_de_asientos": argumentos[3],
                "id_vuelo": argumentos[4]
            })
            update.message.reply_text(
                f"El vuelo {argumentos[4]} para el usuario/a {argumentos[1]} ha sido registrado.")
        except ConnectionException as err:
            print(err)
            update.message.reply_text('Algo ha ocurrido mal.')

    @classmethod
    def buyrtticket(cls, update):
        """ Comprar vuelo con retorno """
        argumentos = update.message['text'].split(" ")[1:]
        if len(argumentos) != 5:
            update.message.reply_text('Debe completar los campos requeridos.')
            return
        try:
            cls.vuelos_collection = cls.db['vuelos']
            cls.usuarios_collection = cls.db['usuarios']
            vuelo = cls.vuelos_collection.find_one(
                {'numero de vuelo': int(argumentos[4])})
            if vuelo['fecha de llegada'] == '':
                update.message.reply_text(
                    'Con este comando solo puede reservar un vuelo con fecha de retorno.')
                return
            cls.usuarios_collection.insert_one({
                "nombre": argumentos[0],
                "apellido": argumentos[1],
                "cedula": argumentos[2],
                "numero_de_asientos": argumentos[3],
                "id_vuelo": argumentos[4]
            })
            update.message.reply_text(
                f"El vuelo {argumentos[4]} para el usuario/a {argumentos[1]} ha sido registrado.")
        except ConnectionException as err:
            print(err)
            update.message.reply_text('Algo ha ocurrido mal.')

    @classmethod
    def unrecognized_command(cls, update):
        """ Comando no reconocido """
        update.message.reply_text(
            'Comando no reconocido. Escriba /help para ver los comandos disponibles.')
    @classmethod
    def unrecognized_input(cls, update):
        """ Entrada no reconocida """
        update.message.reply_text(
            'Solo se admite ingresar comandos. Escriba /help para ver los comandos disponibles.')
    @classmethod
    def metodos(cls):
        """ Inicializacion de los eventos """
        try:
            updater = Updater(cls.TELEGRAM_TOKEN, use_context=True)
            updater.dispatcher.add_handler(
                CommandHandler("start", cls.start))
            updater.dispatcher.add_handler(
                CommandHandler("list", cls.list))
            updater.dispatcher.add_handler(
                CommandHandler("searchd", cls.searchd))
            updater.dispatcher.add_handler(
                CommandHandler("searcho", cls.searcho))
            updater.dispatcher.add_handler(
                CommandHandler("buyticket", cls.buyticket))
            updater.dispatcher.add_handler(
                CommandHandler("buyrtticket", cls.buyrtticket))
            updater.dispatcher.add_handler(
                CommandHandler("help", cls.start))
            updater.dispatcher.add_handler(
                MessageHandler(Filters.command, cls.unrecognized_command))
            updater.dispatcher.add_handler(
                MessageHandler(Filters.all, cls.unrecognized_input))
            updater.start_polling()
            print('Bot funcionando...')
            updater.idle()
        except ConnectionException as err :
            print('Ha ocurrido un error en la conexión con la API de Telegram -> ')
            print(err)


bot = FlyBot()
