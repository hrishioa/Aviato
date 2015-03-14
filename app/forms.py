from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class SearchForm(Form):
    search = StringField("search", validators=[DataRequired()])
