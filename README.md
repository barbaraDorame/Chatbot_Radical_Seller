# Chatbot vendedor de productos milagro

Chatbot con aprendizaje.

## Corriendo el proyecto

Se recomienda correr el servidor en un ambiente virtual de python. Usando solo
virtualenv.

´´´bash
$ virtualenv venv # crea el ambiente virtual
$ source activate venv
´´´

Para instalar las dependencias de python

´´´bash
$ pip -r requirements.txt
$ python -m spacy download es_core_news_sm # Modelo de spacy en español
´´´

Finalmente, corremos el servidor de prueba.

´´´
$ export FLASK_APP=app.py
$ export FLASK_ENV=debug
$ flask run
´´´

## Herramientas:

### Backend
* Python
    * Spacy
    * Flask
    * SKLearn
    * Gensim

### Frontend
* Javascript
* HTML/CSS

## Auxiliares:
#### DB análisis de sentimientos:
* [Spanish DAL: Diccionario de Afectos en Español](http://habla.dc.uba.ar/gravano/sdal.php?lang=esp)  
