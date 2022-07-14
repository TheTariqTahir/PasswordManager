from ast import Break
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCsbcjhdQw31OQeg5KrC7qXQuuvqk7VzWw",
    "authDomain": "passwordmanager-43.firebaseapp.com",
    "projectId": "passwordmanager-43",
    "storageBucket": "passwordmanager-43.appspot.com",
    "messagingSenderId": "419467193948",
    "appId": "1:419467193948:web:04cbbaea7c74e5dfe80099",
    "databaseURL": "https://passwordmanager-43-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

i = {'Category': 'facebook', 'Email': 'dddd', 'Hint': 'aaaa', 'Password': 'fffff', 'fav_icon': 'heart-outline', 'key': '2022-06-01 19:03:12.390339'}
user = 'test'

data = db.child('Users').child(user).child('Categories').child(i['Category']).child('items').get()

for j in data.each():
    if j.val()['key'] == i['key']:
        print(j.val())