import spacy
nlp = spacy.load("es_core_news_md")

class ChatBot:
    def __init__(self, texto):
        self.text = texto


    def limpieza(self, texto):
        texto = texto.lower()
        nlp(texto)


    def responder(self, texto):

    def clasificar(self, texto):

    def analisis_sentimientos(self, texto):

    def procesar(self):
