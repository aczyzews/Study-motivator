import pymysql as p
from datetime import datetime
from ML_model.Model2 import MLPredictor

connection=p.connect(host='localhost',
                     user='adam', #to se zmiencie
                     password='mysecretpassword',#to tez
                     database='flask_project',
                     cursorclass=p.cursors.DictCursor)


def stringformatter(s):
    s = "{}{}{}".format("'", s, "'")
    return s

def addNewUser(nick,password,name,surname):
    cursor=connection.cursor()
    nick=stringformatter(nick)
    password=stringformatter(password)
    name=stringformatter(name)
    surname=stringformatter(surname)
    cursor.execute("insert into user (user_ID_nick,name,surname,password) values({},{},{},{}) ".format(nick,name,surname,password))
    connection.commit()
    cursor.close()


class User:
    def __init__(self,nick):
        cursor=connection.cursor()
        self.nick=stringformatter(nick)
        cursor.execute("select * from user where user_ID_nick={}".format(self.nick))
        self.user_info=cursor.fetchone()
        cursor.close()
        self.goals=Goals(nick)






    def __updateUserInfoFromDB(self):
        cursor=connection.cursor()
        cursor.execute("select * from user where user_ID_nick={}".format(self.nick))
        self.user_info = cursor.fetchone()

        cursor.close()

    def __insertQueryUserInfoUpdateFormatter(self,dictionary):
        s = ""
        for key in dictionary:
            if (dictionary[key] == None or key == 'user_ID_nick' or key=='surname' or key=='name' or key=='password'):
                continue
            try:
                int(dictionary[key])
                s += "{}={},".format(key, dictionary[key])
            except:
                s += "{}='{}',".format(key, dictionary[key])

        s = s[:-1] #remove the last comma
        print(s)
        return s

    def __queryUserInfoUpdateFormatter(self,dictionary):
        print("update user set {} where user_ID_nick={}".format(self.__insertQueryUserInfoUpdateFormatter(dictionary), self.nick))
        return "update user set {} where user_ID_nick={}".format(self.__insertQueryUserInfoUpdateFormatter(dictionary), self.nick)

    def updateUserInformation(self,**kwargs):
        for key in self.user_info:
            if (key in kwargs):
                self.user_info[key]=kwargs[key]
        cursor = connection.cursor()
        cursor.execute(self.__queryUserInfoUpdateFormatter(kwargs))
        connection.commit()
        cursor.close()
        self.__updateUserInfoFromDB()

    def AddPredictionsForNotCompletedGoals(self):
        copy=self.user_info.copy()
        self.goals.addPredictionsForGoals(copy)

import os

class Goals:
    def __init__(self,nick):
        self.nick=nick
        cursor=connection.cursor()
        print("SELECT * FROM goals WHERE end_date < CURRENT_TIMESTAMP AND User_ID={}".format("'"+self.nick+"'"))
        cursor.execute("SELECT * FROM goals WHERE end_date < CURRENT_TIMESTAMP AND User_ID={}".format("'"+self.nick+"'"))
        self.completed_goals=cursor.fetchall()
        print(self.completed_goals)
        cursor.execute("SELECT * FROM goals WHERE end_date >= CURRENT_TIMESTAMP AND User_ID={}".format("'"+self.nick+"'"))
        self.not_completed_goals=cursor.fetchall()
        cursor.close()
        self.MLPredictor = MLPredictor.MLPredictor()


    def DeleteExistingGoal(self,index):
        cursor=connection.cursor()
        print(len(self.not_completed_goals)-index)
        cursor.execute("delete from goals where goal_ID={}".format(self.not_completed_goals[index]['goal_ID']))
        connection.commit()
        cursor.close()
        self.__updateGoalsFromDB()

    def __updateGoalsFromDB(self):
        cursor=connection.cursor()
        cursor.execute("SELECT * FROM goals WHERE end_date < CURRENT_TIMESTAMP;".format(self.nick))
        self.completed_goals = cursor.fetchall()
        cursor.execute("SELECT * FROM goals WHERE end_date >= CURRENT_TIMESTAMP;".format(self.nick))
        self.not_completed_goals = cursor.fetchall()
        cursor.close()

    def addNewGoal(self,type,end_date,start_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")):
        """takes date as datetime(year, month, day, hour, minute, second).strftime("%Y-%m-%d %H:%M:%S")"""
        cursor=connection.cursor()
        cursor.execute("insert into goals values (0,'{}',0.0,{},{},0,{},NULL)".format(self.nick,stringformatter(start_date),stringformatter(end_date),stringformatter(type)))
        connection.commit()
        cursor.close()
        self.__updateGoalsFromDB()


    def modifyEndTimeInNotCompletedGoal(self,index,end_date):
        """takes date as datetime(year, month, day, hour, minute, second).strftime("%Y-%m-%d %H:%M:%S")"""
        goal_ID=self.not_completed_goals[index]["goal_ID"]
        cursor=connection.cursor()
        cursor.execute("update goals set end_date={} where goal_ID={}".format(stringformatter(end_date),goal_ID))
        connection.commit()
        cursor.close()
        self.__updateGoalsFromDB()

    def addStudyHoursToGoal(self,index,number_of_hours):
        if index >= len(self.not_completed_goals) or index < 0:
            return
        self.not_completed_goals[index]['total_time_studied']+=number_of_hours
        self.__calculate_avg(index)
        cursor=connection.cursor()
        cursor.execute("update goals set study_time_week_avg={},total_time_studied={} where goal_ID={}".format(self.not_completed_goals[index]['study_time_week_avg'],self.not_completed_goals[index]['total_time_studied'],self.not_completed_goals[index]['goal_ID']))
        connection.commit()
        cursor.close()
        self.__updateGoalsFromDB()

    def __calculate_avg(self,index):

        self.not_completed_goals[index]['study_time_week_avg']=self.not_completed_goals[index]['total_time_studied']/((datetime.now()-self.not_completed_goals[index]['start_date']).days/7+1)

    def addPredictionsForGoals(self,user_info):
        # calculating score for all not completed goals
        if user_info['sex'] == 'male':
            sex = 1
        else:
            sex = 0
        for goal in self.not_completed_goals:
            type=None
            if goal['type'] == 'math':
                type = 1
            elif goal['type'] == 'language':
                type = 0
            goal['predicted_score'] = self.MLPredictor.predict(sex, user_info['age'], user_info['address'],
                                                               goal['study_time_week_avg'], user_info['freetime'],
                                                               user_info['going_out'],
                                                               user_info['alcohol_drunk_weekly'],
                                                               user_info['alcohol_drunk_weekend'],
                                                               user_info['health'], type)







