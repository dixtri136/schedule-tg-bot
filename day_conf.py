from datetime import datetime, date
from db import DataBase
import re 

db = DataBase("db.db")

def is_even_week():
    week_number = date.today().isocalendar()[1]
    return week_number % 2 == 0

def id_days(schedules):
    today = int(datetime.isoweekday(datetime.now()))
    if is_even_week() == 1:
        if schedules == "schedule_tomorrow":
            txt = db.info_schedule("schedule-tom", today)[0][0]
        elif schedules == "schedule":
            txt = db.info_schedule("schedule", today)[0][0]
    else:
        if schedules == "schedule_tomorrow":
            txt = db.info_schedule("schedule1-tom", today)[0][0]
        elif schedules == "schedule":
            txt = db.info_schedule("schedule1", today)[0][0]
    
    if "[" in txt and "]" in txt:
        index_1 = txt.index("[")
        index_2 = txt.index("]")
        row = re.sub("[,|.]","", txt[index_1+1:index_2])
        txt1 = row.split()
        txt2 = []
        for i in txt1:
            i = int(i)
            txt2.append(i) 
        idi = db.info(txt2)
    elif txt == "99":
        idi = "Розклад не відомий"
    elif txt == "0":
        idi = "Вихідний 🎉"
    return idi