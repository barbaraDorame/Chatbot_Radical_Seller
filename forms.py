from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectField, SubmitField
from wtforms.validators import DataRequired


class ChatForm(FlaskForm):
    id_conversacion = HiddenField('ID de la conversación',
                                  validators=[DataRequired()])
    texto = StringField('Mensaje', validators=[DataRequired()])
    enviar = SubmitField('Enviar')


class ClassifyForm(FlaskForm):
    id_mensaje = HiddenField("ID del mensaje", validators=[DataRequired()])
    texto = StringField('Texto del mensaje', validators=[DataRequired()])
    intencion = SelectField('Intención', validators=[DataRequired()])
    enviar = SubmitField('Enviar')
