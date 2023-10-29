from wtforms.widgets import TextArea
from flask_wtf import FlaskForm
from wtforms.fields import StringField,SubmitField,DateTimeField,PasswordField
from wtforms.validators import DataRequired





class CreatePostForm(FlaskForm):
    post_title=StringField("Post Title",validators=[DataRequired()])
    post_content=StringField("Post Content",validators=[DataRequired()], widget=TextArea())
    submit=SubmitField("Create Post")



class RegisterForm(FlaskForm):
    first_name=StringField("Enter your First name",validators=[DataRequired()])
    last_name=StringField("Enter your Last name",validators=[DataRequired()])
    email_id=StringField("Enter the email id",validators=[DataRequired()])
    password=PasswordField("Enter your Password",validators=[DataRequired()])
    password2=PasswordField("Re-Enter your Password",validators=[DataRequired()])
    submit=SubmitField("Submit")


class LoginForm(FlaskForm):
    email = StringField("Enter your Email ID", validators=[DataRequired()])
    password = PasswordField("Enter the Password", validators=[DataRequired()])
    submit = SubmitField("submit")
