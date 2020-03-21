from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField ,SelectField,TextAreaField
from wtforms.validators import DataRequired, Length, Email
from wtforms.fields.html5 import  DateTimeField

class PartyForm(FlaskForm):
    name = StringField('Party Name', validators=[DataRequired(),Length(min=1, max=255)])
    description = TextAreaField('Description', validators=[DataRequired(),Length(min=1, max=500, message='Max number of 500 charecter')])
    date = DateTimeField('Party Date ', validators=[DataRequired()],format='%Y-%m-%d %H:%M:%S',render_kw={"placeholder": "2020-01-01 10:00:00"})
    submit = SubmitField('Submit')

class PersonForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email('Entre a valid email'),Length(min=1, max=255, message='Max number of 500 charecter')])
    name = StringField('Name', validators=[DataRequired(),Length(min=1, max=255)])
    submit = SubmitField('Submit')