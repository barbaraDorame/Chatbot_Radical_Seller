""" Este modulo incluye el api web para interactuar con el chatbot """
from flask import Flask, request, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from forms import ChatForm, ClassifyForm
import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

app.secret_key = 'HiPoPotamo'


class DummyBot:
    def mensaje_inicial(self):
        return "suh dude"

    def responder(self, text):
        return text[::-1]


class Dialogo(db.Model):
    __tablename__ = 'dialogo'
    id = db.Column(db.Integer, primary_key=True)
    respuesta = db.Column(db.String(255))
    etiqueta = db.Column(db.String(50))
    enojo = db.Column(db.Float)
    feliz = db.Column(db.Float)
    categoria = db.Column(db.String(50))
    producto = db.Column(db.String(50))


class Conversacion(db.Model):
    __tablename__ = 'conversacion'
    id = db.Column(db.Integer, primary_key=True)
    mensajes = db.relationship('Mensaje', backref='conversacion', lazy=True)
    topico = db.Column(db.String(50))


class MensajeBort(Mensaje):
    __tablename__ = 'mensaje_bort'
    id = db.Column(db.Integer, db.ForeignKey('mensaje.id'))
    dialogo_id = db.Column(db.Integer, db.ForeignKey('dialogo.id'))


class Mensaje(db.Model):
    __tablename__ = 'mensaje'
    id = db.Column(db.Integer, primary_key=True)
    hora_creacion = db.Column(db.DateTime, nullable=False,
                              default=datetime.datetime.utcnow)
    id_conversacion = db.Column(db.Integer, db.ForeignKey('conversacion.id'),
                                nullable=True)
    humano = db.Column(db.Boolean, nullable=False, default=False)
    intencion_inferida = db.Column(db.String(255))
    intencion_real = db.Column(db.String(255))
    etiquetado = db.Column(db.Boolean, nullable=False, default=False)
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
mensajes_schema = MensajeSchema(many=True)
conversacion_schema = ConversacionSchema()


def construir_chatbot(conversation):
    """Construye un chatbot correspondiente a la conversacion"""

    return DummyBot()


@app.route('/', methods=('GET', 'POST'))
def index():
    form = ChatForm()
    print(form.texto.data)
    print(form.id_conversacion.data)
    if form.validate_on_submit():
        id_conversacion = int(form.id_conversacion.data)
        texto_humano = form.texto.data
        print('Agregando mensaje')
        conversacion = Conversacion.query.get(id_conversacion)

        print(conversacion)
        mensaje_humano = Mensaje(humano=True, texto=texto_humano)
        conversacion.mensajes.append(mensaje_humano)

        db.session.add(mensaje_humano)

        chatbot = construir_chatbot(conversacion)

        texto_bot = chatbot.responder(texto_humano)
        mensaje_bot = Mensaje(humano=False, texto=texto_bot)
        conversacion.mensajes.append(mensaje_bot)

        db.session.add(mensaje_bot)
    else:
        print('Creando conversación')
        conversacion = Conversacion()
        db.session.add(conversacion)

        bot = construir_chatbot(conversacion)
        texto = bot.mensaje_inicial()
        mensaje = Mensaje(humano=False, texto=texto)
        conversacion.mensajes.append(mensaje)
        db.session.add(mensaje)

    db.session.commit()

    form.id_conversacion.data = conversacion.id
    form.texto.data = ""

    return render_template('index.jinja', conversacion=conversacion,
                           form=form)


@app.route('/etiquetar', methods=('GET', 'POST'))
def clasificar():
    form = ClassifyForm()

    return render_template('classify.jinja', form=form)


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

    return mensajes_schema.jsonify([mensaje_humano, mensaje_bot])
