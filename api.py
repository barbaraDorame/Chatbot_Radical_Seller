""" Este modulo incluye el api web para interactuar con el chatbot """
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from chatbot import ChatBot
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

app.secret_key = 'HiPoPotamo'


class Conversacion(db.Model):
    __tablename__ = 'conversacion'
    id = db.Column(db.Integer, primary_key=True)
    mensajes = db.relationship('Mensaje', backref='conversacion', lazy=True)


class Mensaje(db.Model):
    __tablename__ = 'mensaje'
    id = db.Column(db.Integer, primary_key=True)
    hora_creacion = db.Column(db.DateTime, nullable=False,
                              default=datetime.datetime.utcnow)
    id_conversacion = db.Column(db.Integer, db.ForeignKey('conversacion.id'),
                                nullable=False)
    humano = db.Column(db.Boolean, nullable=False, default=False)
    texto = db.Column(db.String(1000), nullable=False, default="")


class MensajeSchema(ma.ModelSchema):
    class Meta:
        model = Mensaje


class ConversacionSchema(ma.ModelSchema):
    class Meta:
        model = Conversacion

    mensajes = ma.Nested(MensajeSchema, many=True,
                         only=['texto', 'hora_creacion', 'humano'])


mensaje_schema = MensajeSchema()
conversacion_schema = ConversacionSchema()


def construir_chatbot(conversation):
    """Construye un chatbot correspondiente a la conversacion"""

    return ChatBot("")


@app.route('/')
def index():
    return "hi"


@app.route('/api/conversacion', methods=['POST'])
def crear_conversacion():
    """Crea una conversación nueva en la base de datos y la regresa."""
    conversacion = Conversacion()
    db.session.add(conversacion)
    db.session.commit()

    return conversacion_schema.jsonify(conversacion)


@app.route('/api/conversacion/<int:id_conversacion>')
def obtener_conversacion(id_conversacion):
    """Busca una conversacion en la base de datos y la regresa si existe,
       aborta con 404 en otro caso"""

    conversacion = Conversacion.query.get(id_conversacion)

    if conversacion is None:
        return abort(404)

    return conversacion_schema.jsonify(conversacion)


@app.route('/api/conversacion/<int:id_conversacion>/mensajes',
           methods=['POST'])
def conversar(id_conversacion):
    """Agrega un nuevo mensaje del usuario a una conversacion, agrega una
       respuesta generada, y regresa la respuesta generada"""
    conversacion = Conversacion.query.get(id_conversacion)

    if conversacion is None:
        return abort(404)

    texto = request.json.get('texto')
    if texto is None:
        return abort(400)

    mensaje_humano = Mensaje(humano=True, texto=texto,
                             conversacion=conversacion)
    db.session.add(mensaje_humano)

    conversacion.mensajes.append(mensaje_humano)

    chatbot = construir_chatbot(conversacion)

    texto_bot = chatbot.responder(texto)
    mensaje_bot = Mensaje(humano=False, texto=texto_bot)
    db.session.add(mensaje_bot)

    conversacion.mensajes.append(mensaje_bot)

    db.session.commit()

    return mensaje_schema.jsonify(mensaje_bot)
