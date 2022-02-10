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

class UserAuthenticator:
    def __init__(self, nick):
        nick = stringformatter(nick)
        cursor = connection.cursor()
        sqlquery = "select * from user where user_ID_nick={}".format(nick)
        cursor.execute(sqlquery)
        user_dict = cursor.fetchone()
        self.userinfo=user_dict
        cursor.close()

    def authenticate(self,password):

        if(self.userinfo==None):
            return False
        if(password==self.userinfo['password']):
            return True
        return False