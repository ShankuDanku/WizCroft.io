import pyrebase
import datetime

firebaseConfig = {"apiKey": "AIzaSyA4gN1-feLXQWeDWj83LzLG7PiRyOJ89Pw",
                  "authDomain": "dti-project-47ea2.firebaseapp.com",
                  "databaseURL": "https://dti-project-47ea2-default-rtdb.asia-southeast1.firebasedatabase.app",
                  "projectId": "dti-project-47ea2",
                  "storageBucket": "dti-project-47ea2.appspot.com",
                  "messagingSenderId": "953953404444",
                  "appId": "1:953953404444:web:650357f943b10ed16381d9",
                  "measurementId": "G-C39QYQP9SS"}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


def SignUp(username, name, password):
    db.child('Users').child(username).set({'name': name, 'password': password})


def CreateGroup(GroupName, user):
    db.child('Groups').push({'Name': GroupName, 'Organizer': user, 'Active': 'False'})


def CheckGroup(user):
    grps = db.child('Groups').get().val()
    grp = []
    for key in grps:
        if grps[key]['Organizer'] == user:
            grp.append(grps[key]['Name'])
    return grp


def UpdateGroupStatus(id, status):
    db.child('Groups').child(id).update({'Active': status})


def JoinGroup(id, user):
    db.child('Attendees').push({'Group': id, 'User': user})


def CheckAttendee(id, user):
    keys = db.child('Attendees').get().val()
    for key in keys:
        if keys[key]['Group'] == id and keys[key]['User'] == user:
            return True
    return False


def SendAttendance(user, group, present):
    db.child('Timestamps').push(
        {'User': user, 'Group': group, 'Time': str(datetime.datetime.now()), 'Present': str(present)})


def Activate(group):
    key = db.child('Sessions').push({'Group': group, 'Start': str(datetime.datetime.now()), 'End': ''})


def Deactivate(group):
    key = list(db.child('Sessions').order_by_key().get().val().keys())[-1]
    db.child('Sessions').child(key).update({'End': str(datetime.datetime.now())})


def GetSessions():
    return db.child('Sessions').get().val()


def StrToTime(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S.%f")

def GetAttendeeList(group):
    attendees = []
    relation = db.child('Attendees').get().val()
    for key in relation:
        if relation[key]['Group'] == group:
            attendees.append(relation[key]['User'])
    return attendees

# date = datetime.datetime.strptime('2021-11-22 03:27:27.084983', "%Y-%m-%d %H:%M:%S.%f")
# dates = []
# d=date
# while date < d + datetime.timedelta(minutes=1):
#     dates.append(date)
#     date+=datetime.timedelta(seconds=5)
# print(dates)
