from kivy.lang import Builder
from datetime import datetime
from kivymd.app import MDApp
from kivy.metrics import dp, sp
from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.clipboard import Clipboard
from kivy.uix.screenmanager import RiseInTransition, FallOutTransition,SlideTransition
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.clock import Clock
from kivymd.uix.label import MDLabel, MDIcon
from kivy.core.window import Window
import asyncio
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import (
    FakeCircularElevationBehavior,
)


class ClickableMDIcon(ButtonBehavior, MDIcon):
    pass


class LogoCard(FakeCircularElevationBehavior, ButtonBehavior, MDBoxLayout):
    pass

from kivymd.uix.behaviors import RectangularElevationBehavior

class CardMain(RectangularElevationBehavior, MDCard):
    pass



class Category_content(MDBoxLayout):
    # def __init__(self):
    pass

class Eidt_details(MDBoxLayout):
    pass

class Add_Credentials(MDBoxLayout):
    pass


import pyrebase
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
db=firebase.database()
auth_signin = firebase.auth()

#==========amin Firebase
import json
import firebase_admin
from firebase_admin import auth as auth_register
from firebase_admin import credentials
cred = credentials.Certificate("passwordmanager-43-firebase-adminsdk-jivnk-ee21cbbd63.json")
fb =firebase_admin.initialize_app(cred)



class Main(MDApp):
    path_to_kv_file='kv_file.kv'

    def build(self):
        # self.w= Window.size
        self.w=Window.size=350, 650
        self.theme_cls.primary_palette="Teal"
        # self.theme_cls.primary_hue="A700"
        self.theme_cls.primary_hue="500"
        self.theme_cls.theme_style="Light"

        # self.font_name='font/BlaakThin_PERSONAL.ttf'
        self.font_name='font/Roboto-Medium.ttf'


        # text_file=open('hotreloader.kv', 'r')
        # KV=text_file.read()
        # self.builder=Builder.load_string(KV)

        self.builder = Builder.load_file('kv_file.kv')
        self.screen_manager = self.builder.ids.screen_manager
        
        
        self.selected_category='heart'
        self.selected_details={}
        self.user='User1'
        self.password=''

        self.details_page_category=''

        self.edit_email=''
        self.edit_pass=''
        self.edit_hint=''
        self.edit_category=''
        self.key=''
        self.root=None
        self.forgotPage=False
        Window.bind(on_keyboard=self.onBackKey)
        self.count_back=0
        self.screen_list = []
        # self.screen_list.append(self.builder.ids.screen_manager.current)

        # print(self.screen_manager.get_screen('MainPage').ids)
        
        self.spinner=False
        


        return self.builder
    def set_root(self,root):
        self.root=root
        self.root.manager.get_screen('ResetPage').ids.reset_link.clear_widgets()
        
        self.forgotPage=True
        
    def forgot_password(self,email,spinner):
        spinner.active=True
        def forgot_password_(email,spinner):
            if email=='':
                self.show_dialog('Error','Please enter login Email')
                spinner.active=False
            else:
                reset_link = auth_register.generate_password_reset_link(email=email,action_code_settings=None)
                card=MDCard(
                    orientation='vertical',
                    size_hint=(.9,None),
                    height=dp(150),
                    pos_hint={'center_x':.5},
                    elevation=dp(6),
                    radius=dp(20),
                    padding=dp(20),
                )
                
                instruction_label= MDLabel(
                            text='Go to below link to reset your password',
                            theme_text_color='Custom',
                            text_color=self.theme_cls.primary_color,
                            font_size=sp(15)                ,
                            adaptive_height=True,
                            size_hint_y=.5,
                )
                boxLayout=MDBoxLayout(spacing=dp(5))
                link_label=MDLabel(
                    text=reset_link[:50],
                    pos_hint={'center_y':.5},
                    font_size=sp(15),
                )
                copy_icon=ClickableMDIcon(
                                icon='content-copy',
                                halign='right',
                                pos_hint={'center_y':.5},
                                on_press=lambda x ,val=reset_link: self.snackbar_show(val),
                )
                copy_icon.adaptive_size=True
                boxLayout.add_widget(link_label)
                boxLayout.add_widget(copy_icon)
                
                card.add_widget(instruction_label)
                card.add_widget(boxLayout)

                self.root.manager.get_screen('ResetPage').ids.reset_link.add_widget(
                    card
                )
                spinner.active=False
                
        Clock.schedule_once(lambda x,email=email,spinner=spinner:forgot_password_(email,spinner),.5)

 
    # @mainthread
    def login(self,email,password,root,spinner):
            # import time
            # time.sleep(3)
        spinner.active=True
        def login_(email,password,root,spinner):
            email=email.strip()
            password=password.strip()
            # print('done')
            try:
                # user = Clock.schedule_once(lambda x , email=email,password=password:  auth_signin.sign_in_with_email_and_password(email=email,password=password))
                user = auth_signin.sign_in_with_email_and_password(email=email,password=password)
                # print(user['localId'])
                self.user=user['localId']
                # self.show_categories()
                Clock.schedule_once(lambda x: self.show_categories())
                db.child('Users').child(str(self.user)).child('User_info').update(
                        {
                            # 'Email':str(email),
                          'Password':str(password),
                        #   'User_Name':str(self.user),
                        }
                        )
                
                root.manager.transition=SlideTransition()
                root.manager.transition.direction='left'
                root.manager.current='MainContent'
                spinner.active=False
            except Exception as e:
                print(e)
                try:
                    test =json.loads(e.args[1])['error']['errors'][0]
                    reason =test['reason']
                    message =test['message']
                    spinner.active=False
                    self.show_dialog(reason,message)
                except Exception as b:
                    print('pass')
                    spinner.active=False
        Clock.schedule_once(lambda x ,email=email,password=password,root=root,spinner=spinner:login_(email,password,root,spinner),.5)

    def register(self,user,email,password,confirm,root,spinner):
        spinner.active=True
        def register_(user,email,password,confirm,root):
            login=False
            email=email.strip()
            user=user.strip()
            confirm=confirm.strip()
            password=password.strip()
            if password==confirm:
                try:
                    user = auth_register.create_user(email=email,password=password,uid=user)
                    print(user.uid)
                    self.user=user.uid

                    self.password=password
                    

                    db.child('Users').child(str(self.user)).child('User_info').set(
                        {'Email':str(email),
                          'Password':str(password),
                          'User_Name':str(self.user),
                        }
                        )
                    
                    import time
                    now=datetime.now()
                    db.child('Users').child(self.user).child('Categories').child('facebook').child('items').push(
                         {'Email': 'abc@example.com', 'Password': 'examplepassword', 'Hint': 'example hint', 'Category': 'facebook', 'key': str(now)})
                    db.child('Users').child(self.user).child('Categories').child('facebook').child(
                                'info').set({'icon': 'facebook'})
                    time.sleep(.5)
                    db.child('Users').child(self.user).child('Categories').child('google').child('items').push(
                         {'Email': 'abc@example.com', 'Password': 'examplepassword', 'Hint': 'example hint', 'Category': 'google', 'key': str(now)})
                    db.child('Users').child(self.user).child('Categories').child('google').child(
                                'info').set({'icon': 'google'})
                    time.sleep(.5)
                         
                    db.child('Users').child(self.user).child('Categories').child('microsoft').child('items').push(
                         {'Email': 'abc@example.com', 'Password': 'examplepassword', 'Hint': 'example hint', 'Category': 'microsoft', 'key': str(now)})
                    db.child('Users').child(self.user).child('Categories').child('microsoft').child(
                                'info').set({'icon':'microsoft' })
                    time.sleep(.5)
                    self.show_dialog('Success','Account Created\nPlease login.')
                    root.manager.transition=SlideTransition() 
                    root.manager.transition.direction='right'
                    root.manager.current='LoginPage'
                    spinner.active=False
                    

                except Exception as e:
                    # test =json.loads(e.args[1])['error']['errors'][0]
                    # reason =test['reason']
                    # message =test['message']
                    self.show_dialog('error',str(e))
                    print(e)
                    spinner.active=False
                    
                
            else:
                spinner.active=False
                self.show_dialog('Mismatch Password','Password Not Matched')

        Clock.schedule_once(lambda x ,user=user,email=email,password=password,confirm=confirm,root=root:register_(user,email,password,confirm,root),.5)


    def onBackKey(self,window,key,*args):
        # print(self.forgotPage)
        if key == 27 and self.forgotPage==True:
            self.root.manager.transition=SlideTransition()
            self.root.manager.transition.direction='right'
            self.root.manager.current='LoginPage'
            self.forgotPage=False
            return True

            # self.root.current='LoginPage'
            
        else:
            if key == 27 and self.screen_list ==[] and self.count_back ==0:
                self.count_back = 1
                # toast('Press Back Again to exit',duration=1)
                snackbar=Snackbar(
                text='Press Back Again to exit',
                duration=1,
                )
                snackbar.open()
                return True
            if key == 27 and self.screen_list ==[] and self.count_back ==1:
                return False
                
            elif key ==27:
                self.screen_manager.current = self.screen_list.pop()
                print(self.screen_list)
                self.screen_manager.transition.direction='right'
                
            return True
        # return False

    def change_theme_color(self, color, hue):
        self.theme_cls.primary_palette=color
        self.theme_cls.primary_hue=hue

    def change_theme(self):
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style="Light"
            self.theme_cls.primary_palette='Teal'
            self.builder.ids.toolbar.md_bg_color=self.theme_cls.bg_normal

            if self.screen_manager.current == 'MainPage':
                Clock.schedule_once(lambda x: self.show_categories(
                    values=self.all_categories))
            elif self.screen_manager.current == 'DetailsPage':
                self.detailsPage(self.selected_details,
                                 self.details_page_category)
            else:
                pass

        else:
            self.theme_cls.theme_style="Dark"
            self.theme_cls.primary_palette='Orange'
            self.builder.ids.toolbar.md_bg_color=self.theme_cls.bg_normal
            if self.screen_manager.current == 'MainPage':
                Clock.schedule_once(lambda x: self.show_categories(
                    values=self.all_categories))
            elif self.screen_manager.current == 'DetailsPage':
                self.detailsPage(self.selected_details,
                                 self.details_page_category)
            else:
                pass

        # async def get_data():
        #     task = asyncio.create_task(self.show_categories())
        pass

    def add_details(self, val):
        self.screen_list.append('MainPage')
        self.selected_details=val
        for i in self.selected_details.values():
            self.details_page_category=i['Category']

        self.detailsPage(self.selected_details, self.details_page_category)
        # print(self.selected_details)

    def add_credentials(self, hint, email, password):
        if email == '' and email == '':
            self.show_dialog('Warning', 'Email and Password is required')
        elif email == '':
            self.show_dialog('Warning', 'Email is required')
        elif password == '':
            self.show_dialog('Warning', 'Password is required')
        else:
            now=datetime.now()
            data={
                'Email': email,
                'Password': password,
                'Hint': hint,
                'Category': str(self.details_page_category),
                'key': str(now),
                'fav_icon':'heart-outline'
            }
            db.child('Users').child(self.user).child('Categories').child(
                self.details_page_category).child('items').push(data)
            category=self.details_page_category
            self.add_credentials_dialog.dismiss()
            self.refresh_details(category)

    def bottom_navigation(self,item):

        for i in self.builder.ids.bottom_nav.children:
            if i == item:
                i.md_bg_color=self.theme_cls.primary_color
                i.children[0].text_color=self.theme_cls.bg_light
            else:
                i.md_bg_color=self.theme_cls.bg_normal
                i.children[0].text_color=self.theme_cls.primary_color

        

    def change_screen(self, screen):
        # print(screen.text)
        if screen == 'MainPage':
            self.screen_manager.transition=FallOutTransition()
        else:
            # self.screen_list.append(screen)
            self.screen_manager.transition=RiseInTransition()
        self.screen_manager.current=screen
        
        

    def LogOut(self,root):
            root.transition.direction='right'
            root.current='LoginPage'

    def add_category(self, text):
        self.spinner=True
        def add_category_(text):
            if text.text == '':
                print('empty')
            else:
                now=datetime.now()
                self.screen_manager.get_screen(
                    'MainPage').ids.Main_page.clear_widgets()
                db.child('Users').child(self.user).child('Categories').child(
                    (text.text).lower()).child('info').set({'icon': str(self.selected_category)})
                db.child('Users').child(self.user).child('Categories').child((text.text).lower()).child('items').push(
                    {'Email': 'abc@example.com', 'Password': 'examplepassword', 'Hint': 'example hint', 'Category': (text.text).lower(), 'key': str(now)})
                self.selected_category='heart'
                Clock.schedule_once(lambda x: self.show_categories(), .5)
                self.spinner=False

        Clock.schedule_once(lambda x ,text=text :add_category_(text),.5)    
        self.spinner=False
            
    def add_category_dialog(self):
        self.category_dialog=MDDialog(
                type="custom",
                content_cls=Category_content(),
                pos_hint={'center_y': .7},
            )
        self.category_dialog.open()
        
    def edit_details_dialog(self, category, hint, email, password, key):
        self.edit_email=email
        self.edit_pass=password
        self.edit_hint=hint
        self.edit_category=category
        self.edit_key=key
        self.edit_dialog=MDDialog(
                type="custom",
                content_cls=Eidt_details(),
                pos_hint={'center_y': .7},

                height=self.w[1]/4.2,
                radius=[20, ],
                md_bg_color=self.theme_cls.bg_light,
            )
        self.edit_dialog.content_cls.ids.edit_email.text=self.edit_email
        self.edit_dialog.content_cls.ids.edit_hint.text=self.edit_hint
        self.edit_dialog.content_cls.ids.edit_pass.text=self.edit_pass
        self.edit_dialog.content_cls.ids.edit_key.text=self.edit_key
        self.edit_dialog.content_cls.ids.edit_category.text=self.edit_category
        self.edit_dialog.open()

    def add_details_dialog(self):
        self.add_credentials_dialog=MDDialog(
                type="custom",
                content_cls=Add_Credentials(),
                pos_hint={'center_y': .7},
                height=self.w[1]/4.2,
                radius=[20, ],
                md_bg_color=self.theme_cls.bg_light,
            )
        self.add_credentials_dialog.open()

    def update_details(self, edit_key, edit_category, edit_hint, edit_email, edit_pass):
        def update_details_( edit_key, edit_category, edit_hint, edit_email, edit_pass):
            data={
                'Email': edit_email,
                'Password': edit_pass,
                'Hint': edit_hint,

            }
            details=db.child('Users').child(self.user).child(
                'Categories').child(edit_category).child('items').get()
            for i in details.each():
                if i.val()['key'] == edit_key:
                    db.child('Users').child(self.user).child('Categories').child(
                        edit_category).child('items').child(i.key()).update(data)
                    break
            self.edit_dialog.dismiss()
            Clock.schedule_once(
                lambda x, val=edit_category:  self.refresh_details(val))
        Clock.schedule_once(lambda x,  edit_key=edit_key, edit_category=edit_category, edit_hint=edit_hint, edit_email=edit_email, edit_pass=edit_pass:update_details_( edit_key, edit_category, edit_hint, edit_email, edit_pass),.5)

    def text_replace(self, text, limit):
        # print(text.text)
        limit += 1
        if len(text.text) == limit:
            text.text=text.text[:limit-1]
        else:
            pass

    def dismiss_category(self):
        self.category_dialog.dismiss()

    def delete_category(self, deleted_category):
        def delete_category_(deleted_category):
            list_of_categories=db.child('Users').child(
                self.user).child('Categories').get()
            if len(list_of_categories.each()) == 1:
                self.show_dialog('Warning', "At least one Category is required")
            else:
                self.screen_manager.get_screen(
                    'MainPage').ids.Main_page.clear_widgets()
                db.child('Users').child(self.user).child(
                    'Categories').child(deleted_category).remove()
                Clock.schedule_once(lambda x: self.show_categories())
        Clock.schedule_once(lambda x, deleted_category=deleted_category:delete_category_(deleted_category),.5)
        

    def add_to_fav(self,i):
        # print(i)
        # get_fav=db.child("Users").child(self.user).child('Fav').push(i)
        get_fav=db.child("Users").child(self.user).child('Fav').get()

        # print(get_fav)
        for j in get_fav.each():
            # print(i)
            item = j.val()
            if item['key']==i['key']:
                print('match')
                break
            else:
                db.child("Users").child('test').child('Fav').push(i)

    def detailsPage(self, val, category):
        # print(val)
        # print(category)
        self.screen_manager.get_screen(
            'DetailsPage').ids.details_title.text=category.upper()
        value=val

        self.change_screen('DetailsPage')
        self.screen_manager.get_screen(
            'DetailsPage').ids.details.clear_widgets()
        for i in value.values():
            # print(i)
            card=MDCard(
                size_hint_y=None,
                height=(self.w[1]/5),
                elevation=dp(3),
                radius=dp(20),
                padding=dp(13),
                spacing=dp(8),
                orientation='vertical',
            )

            hint_boxlayout=MDBoxLayout(
                        size_hint_y=.4,
                        spacing=dp(15),
                        padding=('0dp', '0dp', '14dp', '0dp'),
                        )

            # ===== Hint Text Area
            hint_label=MDLabel(
                    text=i['Hint'],
                    theme_text_color='Custom',
                    text_color=self.theme_cls.primary_color,
                    font_name=self.font_name,
            )
            hint_label.font_size=sp(15)
            fav_icon=ClickableMDIcon(
                icon=i['fav_icon'],
                size_hint=(None, 1),
                width=dp(25),

                on_press=lambda x, val =i :self.add_to_fav(val),
            )

            fav_icon.font_size=sp(18)

            edit_icon=ClickableMDIcon(
                icon='circle-edit-outline',
                size_hint=(None, 1),
                width=dp(25),

                on_press=lambda x, key=i['key'], category=i['Category'], hint=i['Hint'], email=i['Email'], password=i['Password']: self.edit_details_dialog(
                    category, hint, email, password, key),
            )
            edit_icon.font_size=sp(18)
            delete_icon=ClickableMDIcon(
                icon='delete-outline',
                size_hint=(None, 1),
                width=dp(25),
                on_press=lambda x, key=i['key'], category=i['Category']: self.delete_details(
                    category, key),
            )
            delete_icon.font_size=sp(18)
            hint_boxlayout.add_widget(hint_label)
            hint_boxlayout.add_widget(fav_icon)
            hint_boxlayout.add_widget(edit_icon)
            hint_boxlayout.add_widget(delete_icon)

            # on_press=lambda x,key=i['key'],category= i['Category'], hint= i['Hint'],email= i['Email'],password = i['Password']: self.edit_details_dialog(category,hint,email,password,key),
            # on_press=lambda x ,key=i['key'],category=i['Category']: self.delete_details(category,key),
           # =========== Email
            email_boxlayout=MDBoxLayout(
                size_hint_y=.8,
                spacing=dp(8),
                padding=('0dp', '0dp', '20dp', '0dp'),
           )
            email_icon=ClickableMDIcon(
                icon='email',
                size_hint=(None, 1),
                width=dp(25),

            )
            email_icon.font_size=sp(18)

            email_label=MDLabel(
                text=i['Email'],
                font_name=self.font_name,
            )
            email_label.font_size=sp(15)

            email_copy=ClickableMDIcon(
                icon='content-copy',
                size_hint=(None, 1),
                width=dp(20),
                halign='right',
                on_press=lambda x, val=i['Email']: self.snackbar_show(val)

            )
            email_copy.font_size=sp(18)

            email_boxlayout.add_widget(email_icon)
            email_boxlayout.add_widget(email_label)
            email_boxlayout.add_widget(email_copy)
           # ================== Password
            password_boxlayout=MDBoxLayout(
                size_hint_y=.8,
                spacing=dp(8),
                padding=('0dp', '0dp', '20dp', '0dp'),
           )
            password_icon=ClickableMDIcon(
                icon='key',
                size_hint=(None, 1),
                width=dp(25),

            )
            password_icon.font_size=sp(18)
            password_label=MDLabel(
                text=i['Password'],

                font_name=self.font_name,
            )
            password_label.font_size=sp(15)
            password_copy=ClickableMDIcon(
                icon='content-copy',
                size_hint=(None, 1),
                width=dp(20),
                halign='right',
                on_press=lambda x, val=i['Password']: self.snackbar_show(val)

            )
            password_copy.font_size=sp(18)

            password_boxlayout.add_widget(password_icon)
            password_boxlayout.add_widget(password_label)
            password_boxlayout.add_widget(password_copy)



            card.add_widget(hint_boxlayout)
            card.add_widget(email_boxlayout)
            card.add_widget(password_boxlayout)
            self.screen_manager.get_screen('DetailsPage').ids.details.add_widget(
                card)

    def refresh_details(self, category):
        # self.screen_manager.get_screen('DetailsPage').ids.details.clear_widgets()
        selected=db.child('Users').child(self.user).child(
            'Categories').child(category).get()
        for i in selected.each():
            if i.key() == 'items':
                # print(i.val())
                self.detailsPage(i.val(), category)

    def delete_details(self, category, key):
        selected=db.child('Users').child(self.user).child(
            'Categories').child(category).child('items').get()
        if len(selected.each()) == 1:
            self.show_dialog('Warning', "At least one item is required")
        else:
            for i in selected.each():
                if i.val()['key'] == key:
                    db.child('Users').child(self.user).child('Categories').child(
                        category).child('items').child(i.key()).remove()
                    self.refresh_details(category)
                    return


    def show_categories(self, values=''):

        self.screen_manager.get_screen(
            'MainPage').ids.Main_page.clear_widgets()
        if values == '':
            self.all_categories=db.child('Users').child(
                self.user).child('Categories').get()
        else:
            self.all_categories=values


        for i in self.all_categories.each():
            if i.val()['info']['icon'] == 'Other':
                current_icon='heart'
            else:
                current_icon=i.val()['info']['icon']

            current_category=i.key()

            card=MDCard(
                        size_hint_y=None,
                        elevation=dp(3),
                        radius=dp(20),
                        height=(self.w[1]/8),
                        padding=dp(10)
                        )
            Inner_card=MDCard(
                size_hint_x=.8,
                elevation=0,
                spacing=dp(5),
                md_bg_color=self.theme_cls.bg_light,
                on_press=lambda x, value=i.val(
                )['items']: self.add_details(value),
            )

            # anchor = AnchorLayout()

            icon_card=MDCard(
                elevation=0,
                radius=dp(8),
                size_hint=(.418, .53),
                pos_hint={'center_y': .5},
                padding=0,
                md_bg_color=self.theme_cls.primary_color,
            )
            
            Category_icon=ClickableMDIcon(
                icon=current_icon.lower(),
                # size_hint=(.43, .5),
                halign='center',
                pos_hint={'center_y': .55},
                radius=dp(8),
                # md_bg_color=self.theme_cls.primary_color,

                theme_text_color='Custom',
                text_color=(1, 1, 1, 1),
            )
            Category_icon.font_size=sp(20)

            Category_text=MDLabel(
               text=current_category.upper(),
               font_name=self.font_name,
            )
            Category_text.font_size=sp(10)

            icon_card.add_widget(Category_icon)

            Inner_card.add_widget(icon_card)
            # Inner_card.add_widget(Category_icon)
            Inner_card.add_widget(Category_text)
            card.add_widget(Inner_card)


            delete_icon=ClickableMDIcon(
                icon='delete-outline',
                size_hint=(.15, .4),
                pos_hint={'center_y': .5},

                on_release=lambda x, val=i.key(): self.delete_category(val),
            )
            delete_icon.font_size=sp(18)
            card.add_widget(delete_icon)

            self.screen_manager.get_screen(
                'MainPage').ids.Main_page.add_widget(card)


    def snackbar_show(self, value):
        Clipboard.copy(value)
        self.snackbar=Snackbar(
            text='Copied '+value,
            duration=1,
            )
        self.snackbar.open()


    def update_kv_files(self, text):

        with open(self.path_to_kv_file, "w+") as kv_file:
            kv_file.write(text)



    def show_dialog(self, title, text):
        title=title
        text=text
        cancel_btn_username_dialouge=MDFlatButton(
            text="Okay", on_release=self.close_dialog)
        self.dialog=MDDialog(title=title, text=text, size_hint=(
            0.7, 0.2), buttons=[cancel_btn_username_dialouge])
        self.dialog.open()

    def close_dialog(self, obj):
            self.dialog.dismiss()

    def close_profile_dialog(self, obj):
            self.profile_dialouge.dismiss()

if __name__ == '__main__':
    Main().run()
