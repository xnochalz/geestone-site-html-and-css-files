from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


##WTForm

class RegisterForm(FlaskForm):
    unit = StringField("unit", validators=[DataRequired()])
    facility = StringField("facility", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    patient_name = StringField("patient_name", validators=[DataRequired()])
    patient_age = IntegerField("patient_age", validators=[DataRequired()])
    patient_contact = IntegerField("patient_contact", validators=[DataRequired()])
    type_of_tissue = SelectField("unit", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


