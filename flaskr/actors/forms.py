from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError


class ActorsForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(ActorsForm, self).__init__(*args, **kwargs)

    def validate_first_name(self, first_name):
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        data = first_name.data

        for n in numbers:
            if n in data:
                raise ValidationError("Name must be a String!")

    def validate_last_name(self, last_name):
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        data = last_name.data

        for n in numbers:
            if n in data:
                raise ValidationError("Name must be a String!")

    first_name = StringField(
        'first_name', validators=[DataRequired()]
    )

    last_name = StringField(
        'last_name', validators=[DataRequired()]
    )

    age = IntegerField(
        'age', validators=[DataRequired()]
    )

    gender = SelectField(
        'gender', validators=[DataRequired()],
        choices=[('', 'Select gender'),
                 ('male', 'Male'),
                 ('female', 'Female')]
    )

