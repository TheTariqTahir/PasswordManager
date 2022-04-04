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

data = {

    'Email': 'abc@test.com',
    'Password': 'IamPassword'
}

# db.child('Categories').child('facebook').push(data)


Users = db.child('Users').get()
Categories = db.child('Categories').get()
# print(Users)

users_list = {}

emails_list = []
user_info = []
for i in Users.each():
    users_list[i.key()]=i.val()
    emails_list.append(
        {'email': (i.val())['Email'], 'passwd': (i.val())['Password'],'user_name': (i.val())['UserName']})



def LogIn():
    login = False
    u_email = input('Email: ').strip()
    u_passwd = input('Password: ').strip()
    for i in users_list.values():
        if str(u_email) == str(i['Email']) and str(u_passwd)==str(i['Password']):
            print('User Exist')
            user_info.append(i['UserName'])
            user_info.append(i['Email'])
            user_info.append(i['Password'])
            print(user_info)
            break
        else:
            print('Not Exist')


def Register():
    user_exist = True
    email_exist = True

    u_Name = input('User Name: ').strip()
    for i in users_list:
        if str(i) == str(u_Name):
            print('exist')
            Break
        else:
            user_exist = False
    while user_exist:
        u_Name = input('User Name: ').strip()
        for i in users_list:
            if str(i) == str(u_Name):
                print('exist')
                Break
            else:
                user_exist = False

    email = input('Email: ').strip()
    for i in emails_list:
        if str(i['email']) == str(email):
            print('exist')
            Break
        else:
            email_exist = False
    while email_exist:
        email = input('Email: ').strip()
        for i in emails_list:
            if str(i) == str(email):
                print('exist')
                Break
            else:
                email_exist = False

    psswd1 = input('Password: ')
    psswd2 = input('Re-Password: ')
    if str(psswd1) != str(psswd2):
        return print('Password Not matched')
    else:
        passwd = psswd1

    data = {
        "UserName":u_Name,
        "Email": email,
        "Password": passwd
    }
    db.child('Users').child(u_Name).set(data)

# Register()
LogIn()