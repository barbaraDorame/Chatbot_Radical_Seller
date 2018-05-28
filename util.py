import json

def leer_configuracion(dir_archivo):
    with open(dir_archivo, 'r') as fp:
        config = json.load(fp)

    return config
