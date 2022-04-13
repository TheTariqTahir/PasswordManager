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


# res =db.child('Users').get()
# for i in res.each():
#     print(i.val())
categ = db.child('Users').child('User1').child('Categories').get()

for i in categ.each():
    print(i.val())


db.child('Users').child('User1').child('Categories').child('google').child('info').set({'icon':'google'})
from datetime import datetime
now = datetime.now()
print(now)
db.child('Users').child('User1').child('Categories').child('google').child('items').push({'Email':'abc@example.com','Password':'examplepassword','Hint':'example hint','Category':'google','key':str(now)})


# data = {

#     'Email': 'abc@test.com',
#     'Password': 'IamPassword',
#     'Hint':'I am Hint',

# }


# db.child('Categories').child('facebook').push(data)


# Users = db.child('Users').get()
# Categories = db.child('Categories').get()
# print(Users)

# db.child('Users').child('User1').child('Categories').set('Google')
# categ = db.child('Users').child('User1').child('Categories').child('google').delete({'Email':'abc'})

# delete_data = db.child('Users').child('User1').child('Categories').child('google').push({'Email':'abc@example.com','Password':'examplepassword','Hint':'example hint'})

# delete_data = db.child('Users').child('User1').child('Categories').child('google').get()
# for i in delete_data.each():
#     print(i.key())
#     db.child('Users').child('User1').child('Categories').child('google').child(i.key()).remove()

# for i in categ.each():
#     print(i.key())

# db.child('Users').child('User1').child('Categories').child('facebook').child('info').set({'name':'text','icon':'icon'})
# categ = db.child('Users').child('User1').child('Categories').child('google').child('items').get()


# for i in categ.each():
#     print(i.val()['Email'])
    # for j in i.val():


users_list = {}

emails_list = []
user_info = []
# for i in Users.each():
#     users_list[i.key()]=i.val()
#     emails_list.append(
#         {'email': (i.val())['Email'], 'passwd': (i.val())['Password'],'user_name': (i.val())['UserName']})

# print(users_list.keys())

# user = 'User1'
# categ = db.child('Users').child(user).child('Categories').get()

# for i in categ.each():
#     current_category = i.key()
#     print(current_category)
# for j in a:
#     print(j['Email'])
# for i in users_list.values():
#     user_info.append(i['UserName'])
#     user_info.append(i['Email'])
#     user_info.append(i['Password'])


# data = {
#     'Email':"a@b.com",
#     "Password":'asdfasdf',
#     "Remarks": 'i am something',
# }

# db.child('Categories').child('User1').child('Categories').child('facebook').push(data)


# def LogIn():
#     login = False
#     u_email = input('Email: ').strip()
#     u_passwd = input('Password: ').strip()
#     for i in users_list.values():
#         if str(u_email) == str(i['Email']) and str(u_passwd)==str(i['Password']):
#             print('User Exist')
#             user_info.append(i['UserName'])
#             user_info.append(i['Email'])
#             user_info.append(i['Password'])
#             print(user_info)
#             break
#         else:
#             print('Not Exist')


# def Register():
#     user_exist = True
#     email_exist = True

#     u_Name = input('User Name: ').strip()
#     for i in users_list:
#         if str(i) == str(u_Name):
#             print('exist')
#             Break
#         else:
#             user_exist = False
#     while user_exist:
#         u_Name = input('User Name: ').strip()
#         for i in users_list:
#             if str(i) == str(u_Name):
#                 print('exist')
#                 Break
#             else:
#                 user_exist = False

#     email = input('Email: ').strip()
#     for i in emails_list:
#         if str(i['email']) == str(email):
#             print('exist')
#             Break
#         else:
#             email_exist = False
#     while email_exist:
#         email = input('Email: ').strip()
#         for i in emails_list:
#             if str(i) == str(email):
#                 print('exist')
#                 Break
#             else:
#                 email_exist = False

#     psswd1 = input('Password: ')
#     psswd2 = input('Re-Password: ')
#     if str(psswd1) != str(psswd2):
#         return print('Password Not matched')
#     else:
#         passwd = psswd1

#     data = {
#         "UserName":u_Name,
#         "Email": email,
#         "Password": passwd
#     }
#     db.child('Users').child(u_Name).set(data)

# Register()
# LogIn()
