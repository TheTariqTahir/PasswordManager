import pyrebase
import json
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
cred = credentials.Certificate("passwordmanager-43-firebase-adminsdk-jivnk-ee21cbbd63.json")
fb =firebase_admin.initialize_app(cred)



firebaseConfig={
    "apiKey": "AIzaSyCsbcjhdQw31OQeg5KrC7qXQuuvqk7VzWw",
    "authDomain": "passwordmanager-43.firebaseapp.com",
    "projectId": "passwordmanager-43",
    "storageBucket": "passwordmanager-43.appspot.com",
    "messagingSenderId": "419467193948",
    "appId": "1:419467193948:web:04cbbaea7c74e5dfe80099",
    "databaseURL": "https://passwordmanager-43-default-rtdb.firebaseio.com/"
}
firebase=pyrebase.initialize_app(firebaseConfig)
auth2 = firebase.auth()
db = firebase.database()

# user = (auth.get_user_by_email(email='a@b.com'))

# email=input('Enter Email: ')
# password=input('Enter Password: ')
# userid=input('Enter User Name: ')
# user=''
# try:
#     user = auth.create_user(email=email,password=password,uid=userid)
#     # user = auth2.create_user_with_email_and_password(email=email,password=password)
#     print(user.uid)
# except Exception as e:
#     print(e)
    
    # test =json.loads(e.args[1])['error']['errors'][0]
    # reason =test['reason']
    # message =test['message']
    # print(reason,message)

# from datetime import datetime
# now=datetime.now()
# db.child('Users').child('user2').child('Categories').child('Facebook').child('items').push(
#                          {'Email': 'abc@example.com', 'Password': 'examplepassword', 'Hint': 'example hint', 'Category': 'facebook', 'key': str(now)})
# db.child('Users').child('user2').child('Categories').child(
#         'facebook').child('info').set({'icon': 'facebook'})

# print(f'User Created: {user.uid}')

# print(auth.generate_password_reset_link(email='thetariqtahir43@gmail.com',action_code_settings=None))

# auth.delete_user(uid='abc')
# email = 'a@b.com'
# password='abc123'
email = 'thetariqtahir43@gmail.com'
password='rspucnrmpa'

try:
    user = auth2.sign_in_with_email_and_password(email=email,password=password)
    print(user['localId'])
    # for i in user:
    #     print(i)
except Exception as e:
    test =json.loads(e.args[1])['error']['errors'][0]
    reason =test['reason']
    message =test['message']
    print(reason,message)

    


# page = auth.list_users()
# while page:
#     for u in page.users:
#         print(f'User : {u.uid}')
        
#     page = page.get_next_page()




# fb =firebase_admin.initialize_app(firebaseConfig)



# db=firebase.database()

# data = {
#     'User_Name':'Abc123',
#     'Email': 'a@b.com',
#     'Password': '123123'

# }

# db.child('Categories').child('facebook').push(data)

# print(db.child('Users').child('User1').child('Categories').get())

# Users = db.child('Users').child('User1').child('User_Info').set(data)


# Categories = db.child('Categories').get()
# print(Users)

# users_list = {}

# emails_list = []
# user_info = {}
# for i in Users.each():
#     print(i.val()['User_Info']['Email'])
#     print(i.key())
    # users_list[i.key()]=i.val()
    # user_info[i.key()]=(i.val()['User_Info'])

    # emails_list.append(
    #     {'email': (i.val())['Email'], 'passwd': (i.val())['Password'],'user_name': (i.val())['UserName']})
# for i in emails_list:
#     print(i)

# print(users_list('User1'))
# # print(user_info)
# for i in user_info.values():
#     emails_list.append(
#         {'Email': (i)['Email'], 'Password': (i)['Password'],'User_Name': (i)['User_Name']})

# for i in emails_list:
#     print(i['Email'])

def LogIn():
    login = False
    u_email = input('Email: ').strip()
    u_passwd = input('Password: ').strip()
    for i in users_list:
        if str(u_email) == str(i['Email']) and str(u_passwd)==str(i['Password']):
            print('User Exist')
            
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
# LogIn()