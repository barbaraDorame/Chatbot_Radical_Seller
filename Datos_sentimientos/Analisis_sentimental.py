from gensim import corpora, models, similarities
from gensim.corpora import Dictionary

with open('Negativas.txt', 'r') as f:
    negativas = f.read()

with open('Positivas.txt', 'r') as fi:
    positivas = fi.read()

def procesar_sentimientos(texto):
    texto = [texto, [""]]
    dictionary = Dictionary(texto)
    corpus = [dictionary.doc2bow(palabra) for palabra in texto]

    vec_positivo = dictionary.doc2bow(positivas.lower().split())
    vec_negativo = dictionary.doc2bow(negativas.lower().split())

    tfidf = models.TfidfModel(corpus)
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=12)
    porcentaje_positivo = index[tfidf[vec_positivo]]
    porcentaje_negativo = index[tfidf[vec_negativo]]
    valorpos = (list(enumerate(porcentaje_positivo))[0][1])
    valorneg = (list(enumerate(porcentaje_negativo))[0][1])

    if valorpos >= valorneg:
        return valorpos
    else:
        return valorneg
