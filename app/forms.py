from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class RsForm(Form):
    conversion_query = StringField('conversion_query', validators=[DataRequired()])


