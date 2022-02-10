from unittest import TestCase
from DataAccess.GoalAdder import GoalAdder
import pymysql as p
from DataAccess.User import User

connection=p.connect(host='localhost',
                     user='adam',
                     password='mysecretpassword',
                     database='ifeproject',
                     cursorclass=p.cursors.DictCursor)

class TestGoalAdder(TestCase):

    def test_goal(self):
        GoalAdder("math","123")
        cursor = connection.cursor()
        sqlquery = "select * from goal"
        cursor.execute(sqlquery)
        dict = cursor.fetchone()
        self.assertEqual(dict["type"],"math")





