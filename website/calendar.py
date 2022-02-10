from datetime import datetime

from flask import Blueprint, render_template,g, session,request
from DataAccess2.DataContext import User
calendar = Blueprint('calendar', __name__)


@calendar.route('/calendar',methods=["GET","POST"])
def calendar1():
    if g.user:

        user=User(session['nick'])
        user.AddPredictionsForNotCompletedGoals()
        if request.method=="POST":
            if request.form['submit'] == 'delete_goal':

                goalid = int(request.form['goal_id'])
                user.goals.DeleteExistingGoal(goalid-1)

                user.AddPredictionsForNotCompletedGoals()
            if request.form['submit'] == 'modify_end_datetime':

                goalid = int(request.form['goalid'])
                end_datetime_not_converted = request.form['end-date']
                end_datetime=datetime(*[int(v) for v in end_datetime_not_converted.replace('T', '-').replace(':', '-').split('-')])
                user.goals.modifyEndTimeInNotCompletedGoal(goalid-1,end_datetime)

                user.AddPredictionsForNotCompletedGoals()

            if request.form['submit']=='add_study_hours':
                study_hours=int(request.form['hour'])
                goalid=int(request.form['goalid'])
                user.goals.addStudyHoursToGoal(goalid-1,study_hours)
                user.AddPredictionsForNotCompletedGoals()




            if request.form['submit']=='submit_new_goal':
                new_goal_type=request.form['categories']
                start_datetime_not_converted=request.form['start-date']
                end_datetime_not_converted=request.form['end-date']
                start_datetime=datetime(*[int(v) for v in start_datetime_not_converted.replace('T', '-').replace(':', '-').split('-')])
                end_datetime=datetime(*[int(v) for v in end_datetime_not_converted.replace('T', '-').replace(':', '-').split('-')])
                user.goals.addNewGoal(new_goal_type,end_datetime,start_datetime)
                user.AddPredictionsForNotCompletedGoals()
        return render_template("calendar.html",user=user.user_info['name'],not_completed_goals=user.goals.not_completed_goals, completed_goals=user.goals.completed_goals)

@calendar.before_request
def before_request():
    g.user='test'
    if 'nick' in session:
       g.user=session['nick']