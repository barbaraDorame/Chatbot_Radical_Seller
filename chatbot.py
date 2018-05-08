import spacy
from analisis_sentimental import procesar_sentimientos
from clasificador_intencion import ClasificadorIntencion

# Carga el modelo de Spacy para palabras en español
nlp = spacy.load("es_core_news_sm")


class ChatBot:
    '''
    Clase para un chatbot generico
    '''
    def __init__(self, nom_clas):
        '''
        texto es una lista de diccionario, cuyos elementos son:
            Respuesta: String
            Etiqueta: String
            (Saludos, Despedida, Vender, Terminar)
            Enojo: int
            Feliz: int
        '''

        self.clasificador_intencion = ClasificadorIntencion.cargar(nom_clas)
        # Numero de respuestas positivas dadas por el usuario
        self.positivo = 0
        # Numero de respuestas negativas dadas por el usuario
        self.negativo = 0
        # Numero maximo de respuestas negativas que el bot aguanta
        self.fatiga = -1
        self.usuario_positividad = 0

    def limpieza(self, texto):
        '''
        Limpieza de la respuesta dada por el usuario
        '''
        texto = texto.lower()
        texto2 = nlp(texto)
        return texto2

    def responder(self, texto):
        '''
        Regresa la respuesta del bot
        '''
        doc = self.limpieza(texto)
        sent = self.analisis_sentimientos(doc)
        intencion, _ = self.clasificador_intencion.predecir(doc)

        # lex = self.limpieza(texto)
        # self.analisis_sentimientos(lex)
        respuesta = ""
        return respuesta

    def obtener_intencion(self, texto):
        '''
        Trata de inferir la intención de un mensaje
        '''
        pass

    def analisis_sentimientos(self, texto):
        '''
        Manda a llamar a la función que hace el análisis sentimental
        de una respuesta dada por el usuario contra una lista de palabras
        positivas y negativas
        '''
        self.usuario_positividad += procesar_sentimientos(texto)
