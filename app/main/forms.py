from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Required


class VisitForm(FlaskForm):
    purpose = TextAreaField("What is your project for today?",
                            validators=[Required()])
    submit = SubmitField('Submit')
