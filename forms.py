from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, IntegerField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField



##WTForm

class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


class RegisterForm(FlaskForm):
    unit = StringField("unit", validators=[DataRequired()])
    facility = StringField("facility", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    patient_name = StringField("patient_name", validators=[DataRequired()])
    patient_age = IntegerField("patient_age", validators=[DataRequired()])
    patient_contact = IntegerField("patient_contact", validators=[DataRequired()])
    type_of_tissue = SelectField("unit", validators=[DataRequired()])
    cough = SelectField("cough", validators=[DataRequired()])
    dysponia = SelectField("dysponia", validators=[DataRequired()])
    catarrh = SelectField("catarrh", validators=[DataRequired()])
    environmental_factors = SelectField("environmental_factors", validators=[DataRequired()])
    nose_pains = SelectField("nose_pains", validators=[DataRequired()])
    smoking = SelectField("smoking", validators=[DataRequired()])
    chest_pain = SelectField("chest_pain", validators=[DataRequired()])
    chest_xray = SelectField("chest_xray", validators=[DataRequired()])
    psychological_factors = SelectField("psychological_factors", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")


class CommentForm(FlaskForm):
    comment_text = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit Comment")