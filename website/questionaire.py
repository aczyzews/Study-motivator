from flask import Blueprint, render_template,g,session,request,redirect,url_for

questionaire = Blueprint('questionaire', __name__)
from DataAccess2 import DataContext as DC


@questionaire.route('/questionaire',methods=["GET","POST"])
def questionaire1():
    if g.user:
        user = DC.User(session['nick'])
        if request.method == "POST":
            age=request.form["age"]
            sex = request.form["age"]
            if request.form["address"] == "In the countryside":
                address = 1
            else:
                address = 0
            freetime = request.form["freetime"]
            goout = request.form["goout"]
            health_rate = request.form["health-rate"]
            # physical_state = request.form["physical-state"] #doesnt go to database right now (for ML also)
            alcohol_week = request.form["alcohol-week"]
            alcohol_weekend = request.form["alcohol-weekend"]

            user.updateUserInformation(age=age, sex=sex, address=address, freetime=freetime, going_out=goout, alcohol_drunk_weekly=alcohol_week, alcohol_drunk_weekend=alcohol_weekend, health=health_rate)
            return redirect(url_for('calendar.calendar1'))

        return render_template("questionaire.html")



@questionaire.before_request
def before_request():
    if 'nick' in session:
       g.user=session['nick']