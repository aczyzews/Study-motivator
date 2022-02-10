from flask import Blueprint, render_template, request,redirect,url_for,session,flash

import DataAccess2.DataContext as DC
from DataAccess2.UserAuthenticator import UserAuthenticator

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET","POST"])
def login():
    if request.method=="POST":
        session.pop('user',None)
        nick=request.form["username"]
        password=request.form["password"]
        if(UserAuthenticator(nick).authenticate(password)):
            session["nick"]=nick
            return redirect(url_for('calendar.calendar1'))
        else:
            return redirect(url_for('auth.register'))

    else:
        return render_template("login.html")


@auth.route('/logout')
def logout():
    session.pop('nick', None)
    return render_template('index.html')






@auth.route('/register',methods=["GET","POST"])
def register():
    if request.method=="POST":
        nick=request.form["Rusername"]
        password=request.form["Rpassword"]
        name=request.form["Rname"]
        surname = request.form["Rsurname"]
        DC.addNewUser(nick=nick,password=password,name=name,surname=surname)
        session["nick"] = nick
        return redirect(url_for('questionaire.questionaire1'))
    else:
        return render_template("register.html")
