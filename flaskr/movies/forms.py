from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError


class MoviesForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        kwargs['csrf_enabled'] = False
        super(MoviesForm, self).__init__(*args, **kwargs)

    def validate_release_date(self, release_date):
        rd = release_date.data
        if not datetime.strptime(rd, '%Y-%m-%d %H:%M'):
            raise ValidationError("Release Date must be a DateTime(YYYY-MM-DD HH:MM)")

    title = StringField(
        'title', validators=[DataRequired()]
    )

    release_date = StringField(
        'release_date', validators=[DataRequired()],
    )

