from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, RadioField
from wtforms.validators import Required


class VisitForm(FlaskForm):
    purpose = TextAreaField("What is your project for today?",
                            validators=[Required()])
    type_visit = RadioField("What are you here for?",
                            choices=[('work', 'Work'),
                                     ('fun', 'Fun'),
                                     ('class', 'Class')],
                            validators=[Required()])
    submit = SubmitField('Submit')
