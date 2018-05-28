from app import db, Dialogo
import json


def limpieza():
    with open("../conversacion.json") as h:
        dialogos = json.load(h)

    for mono in dialogos:
        logo = Dialogo(respuesta=mono["respuesta"], etiqueta=mono["etiqueta"],
                       enojo=mono["enojo"], feliz=mono["feliz"],
                       categoria=mono["categoria"], producto=mono["producto"])
        db.session.add(logo)

    db.session.commit()
