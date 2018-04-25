import spacy
from Datos_sentimientos.Analisis_sentimental import procesar_sentimientos

nlp = spacy.load("es_core_news_sm")

class ChatBot:
    def __init__(self, texto):
        self.text = texto


    def limpieza(self, texto):
        texto = texto.lower()
        texto2 = nlp(texto)
        return texto2


    def responder(self, texto):

    def clasificar(self, texto):

    def analisis_sentimientos(self, texto):
        procesar_sentimientos(texto)


    def procesar(self, texto):
        lex = self.limpieza(texto)
        self.analisis_sentimientos(lex)
