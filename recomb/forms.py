'''Creates the form to send the file'''
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired

class FormNFe(FlaskForm):
    '''Class representing the form for file selection and the submit button.'''
    botao_NFe = FileField("NFe", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Enviar")
    