from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required


class VisitForm(FlaskForm):
    purpose = TextAreaField("What are you visiting to do?",
                            validators=[Required()])
    submir = SubmitField('Submit')
