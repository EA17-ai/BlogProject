from flask import Flask, render_template,flash,redirect,session, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired
from db import add_post_to_db, check_email, check_password, get_all_user_posts, get_all_users, getlastpost,user_insert
from datetime import datetime
import os
from dotenv import load_dotenv,find_dotenv
from werkzeug.security import check_password_hash,generate_password_hash
from wtforms.widgets import TextArea
from forms import RegisterForm,LoginForm,CreatePostForm

app = Flask(__name__)
_ = load_dotenv(find_dotenv())

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

is_authenticated=False


# Invalid URL

@app.errorhandler(401)
def page_not_found(e):
    return render_template("404.html"), 401

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# Home Page
@app.route("/")
def home():
    global is_authenticated
    if "user_id" in session:
        is_authenticated=True
        first_name=session["first_name"]
        last_name=session["last_name"]
        print(first_name," ",last_name)
        return render_template("home.html",is_authenticated=is_authenticated,first_name=first_name,last_name=last_name)
    else:
        return render_template("home.html",is_authenticated=is_authenticated)
    


@app.route("/register",methods=["GET","POST"])
def register():
    global is_authenticated
    is_authenticated=False
    first_name=None
    last_name=None
    email_id=None
    password1=None
    password2=None
    registerform=RegisterForm()
    if registerform.validate_on_submit():
        first_name=registerform.first_name.data
        last_name=registerform.last_name.data
        email_id=registerform.email_id.data
        password1=registerform.password.data
        password2=registerform.password2.data
        mail_exists=check_email(email_id=email_id)
        if mail_exists:
            flash("Email ID ALREADY EXISTS...Registration not successful")
            registerform.first_name.data=""
            registerform.last_name.data=""
            registerform.email_id.data=""
            registerform.password.data=""
            registerform.password2.data=""
            return render_template("register.html",registerform=registerform,is_authenticated=is_authenticated)
        else:
            if password1==password2:
                user_insert(first_name=first_name,last_name=last_name,email_id=email_id,password=generate_password_hash(password1))
                flash("Registration Successful")
                registerform.first_name.data=""
                registerform.last_name.data=""
                registerform.email_id.data=""
                registerform.password.data=""
                registerform.password2.data=""
                return render_template("register.html",registerform=registerform,is_authenticated=is_authenticated)
            
            else:
                flash("Passwords Doesnt Match.Please register again")    
                return render_template("register.html",registerform=registerform)
    return render_template("register.html",registerform=registerform,is_authenticated=is_authenticated)








@app.route("/createpost",methods=["GET","POST"])
def createpost():
    if "user_id" in session:
        global is_authenticated
        
        first_name=session["first_name"]
        last_name=session["last_name"]
        user_id=int(session["user_id"])
        post_id=int(getlastpost())+1
        post_title=None
        post_content=None
        postform=CreatePostForm()
        if postform.validate_on_submit():
            post_title=postform.post_title.data
            post_content=postform.post_content.data
            add_post_to_db(user_id=user_id,post_id=post_id,post_title=post_title,post_content=post_content,date_added=datetime.now())
            postform.post_title.data=""
            postform.post_content.data=""        
        return render_template("createpost.html",form=postform,is_authenticated=True,first_name=first_name,last_name=last_name)    
    else:
        return render_template("auth.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    global is_authenticated
    
    email = None
    password=None
    form = LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        mail_exists=check_email(email_id=email)
        if mail_exists:
            correct_password,user_id,first_name,last_name,email_id=check_password(email,password)

            print("User id is",user_id)
            
            if correct_password:
                session["user_id"]=user_id
                is_authenticated=True
                session["first_name"]=first_name
                session["last_name"]=last_name
                session["email_id"]=email_id
                #return render_template("loginsuccess.html",is_authenticated=is_authenticated,all_specific_posts=all_specific_posts)
                return redirect(url_for("posts"))
            else:
                flash("Please Check the Credentials")
                return render_template("login.html", form=form, email=email,is_authenticated=is_authenticated)
    return render_template("login.html", form=form, email=email,is_authenticated=is_authenticated)

#print all Registered Users
@app.route("/users")
def users():
    
    global is_authenticated
    if "user_id" in session:
        is_authenticated
        users=get_all_users()
        first_name=session["first_name"]
        last_name=session["last_name"]
        
    #print(users)
        return render_template("users.html",users=users,is_authenticated=is_authenticated,first_name=first_name,last_name=last_name)
    else:
        is_authenticated=False
        return render_template("auth.html",is_authenticated=is_authenticated)

@app.route("/posts")
def posts():
    

    global is_authenticated
    if "user_id" in session:
        all_specific_posts=get_all_user_posts(user_id=int(session["user_id"]))
        first_name=session["first_name"]
        last_name=session["last_name"]

        return render_template("posts.html",all_specific_posts=all_specific_posts,is_authenticated=is_authenticated,first_name=first_name,last_name=last_name)
    else:
        return render_template("auth.html",is_authenticated=False)






@app.route("/logout")
def logout():
    
    global is_authenticated
    if "user_id" in session:
        session.pop("user_id")
        session.pop("first_name")
        session.pop("last_name")
        session.pop("email_id")
        is_authenticated=False
        
        return render_template("logout.html",is_authenticated=is_authenticated)
    else:
        return render_template("logoutalready.html",is_authenticated=False)
    





if __name__ == "__main__":
    app.run(debug=True)
