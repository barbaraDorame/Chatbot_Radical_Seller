import json
from collections import defaultdict

with open('../conversacion.json') as json_file:
    data = json.load(json_file)
for respuesta in data:
    categoria = respuesta["categoria"]
    lista = defaultdict()
    if categoria == "saludo":
        
    elif categoria == "vender":

    elif categoria == "oferta":

    elif categoria == "despedida":

    else:

    return lista
