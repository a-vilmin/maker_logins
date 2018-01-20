from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, RadioField, StringField, \
    FileField
from wtforms.validators import Required, Length
from flask_wtf.file import FileRequired


class VisitForm(FlaskForm):
    purpose = TextAreaField("What is your project for today?",
                            validators=[Required()])
    type_visit = RadioField("What are you here for?",
                            choices=[('work', 'Work'),
                                     ('fun', 'Fun'),
                                     ('class', 'Class')],
                            validators=[Required()])
    submit = SubmitField('Submit')


class AdminSearchForm(FlaskForm):
    name_search = StringField('Email to upgrade', validators=[Required(),
                                                              Length(1, 64)])
    submit = SubmitField('Search name')


class AdminChangeForm(FlaskForm):
    first_name = StringField('First name of new admin to display on user page',
                             validators=[Required(),
                                         Length(1, 64)])
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('Make admin')
