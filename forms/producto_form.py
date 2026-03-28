from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre del Calzado', validators=[DataRequired()])
    marca = StringField('Marca (Nike, Adidas, etc.)', validators=[DataRequired()])
    precio = DecimalField('Precio', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    submit = SubmitField('Guardar')
    