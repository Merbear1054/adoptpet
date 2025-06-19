from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Optional, URL, NumberRange
from flask_wtf.file import FileField, FileAllowed

class AddPetForm(FlaskForm):
    name = StringField("Pet Name", validators=[InputRequired()])
    species = SelectField("Species", choices=[
        ("cat", "Cat"),
        ("dog", "Dog"),
        ("porcupine", "Porcupine")
    ], validators=[InputRequired()])
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=30)])
    notes = TextAreaField("Notes", validators=[Optional()])
    photo_file = FileField("Upload Photo", validators=[Optional(), FileAllowed(["jpg", "png", "jpeg", "gif"], "Images only!")])

from wtforms import BooleanField

class EditPetForm(FlaskForm):
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    notes = TextAreaField("Notes", validators=[Optional()])
    available = BooleanField("Available?")
    photo_file = FileField("Upload New Photo", validators=[Optional(), FileAllowed(["jpg", "png", "jpeg", "gif"], "Images only!")])
