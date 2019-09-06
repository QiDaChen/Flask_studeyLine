from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
class LoginForm(FlaskForm):
    account = StringField(
        lable = "账号"
    )