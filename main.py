
from kivy.lang import Builder
from datetime import datetime
from kivymd.app import MDApp
from kivy.metrics import dp, sp
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton,MDIconButton
from kivy.clock import Clock
from kivymd.uix.label import MDLabel, MDIcon
from kivy.core.window import Window

from kivy.uix.behaviors import ButtonBehavior

class ClickableMDIcon(ButtonBehavior, MDIcon):
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



class Main(MDApp):
    path_to_kv_file='kv_file.kv'
    
    def build(self):
        #self.w= Window.size 
        self.w= Window.size = 350,600
        self.theme_cls.primary_palette = "Indigo"
        self.theme_cls.primary_hue = "A700"
        self.theme_cls.theme_style = "Light"
        
        self.font = 'font/BlaakThin_PERSONAL.ttf'

        
        text_file = open('hotreloader.kv','r')
        KV= text_file.read()
        self.builder = Builder.load_string(KV)
        # self.builder = Builder.load_file('kv_file.kv')
        # self.screen_manager = self.builder.ids.screen_manager
        
        self.selected_category=''
        self.selected_details={}
        self.user = 'User1'
        
        self.details_page_category=''
        
        self.edit_email=''
        self.edit_pass=''
        self.edit_hint=''
        self.edit_category=''
        self.key=''
        
        # self.custom_bg=self.theme_cls.bg_light
        # print(self.screen_manager.get_screen('MainPage').ids)
        
        # Clock.schedule_once(lambda x: self.show_categories())
        
        
        return self.builder

    def change_theme(self):
        if self.theme_cls.theme_style =="Dark":
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_hue = "900"
        else:
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_hue = "A100"
            
        # async def get_data():
        #     task = asyncio.create_task(self.show_categories())
        pass
    
    def add_details(self,val):
        
        self.selected_details=val
        for i in self.selected_details.values():
            self.details_page_category=i['Category']
        self.detailsPage(val,self.details_page_category)
        # print(self.selected_details)
    
    def add_credentials(self,hint,email,password):
        if email =='' and email=='':
            self.show_dialog('Warning','Email and Password is required')
        elif email =='':
            self.show_dialog('Warning','Email is required')
        elif password =='':
            self.show_dialog('Warning','Password is required')
        else:
            now =datetime.now()
            data  = {
                'Email':email,
                'Password':password,
                'Hint':hint,
                'Category':str(self.details_page_category),
                'key':str(now)           
            }
            db.child('Users').child(self.user).child('Categories').child(self.details_page_category).child('items').push(data)
            category = self.details_page_category
            self.add_credentials_dialog.dismiss()
            self.refresh_details(category)
    
    def test(self):
      
        
        print(self.screen_manager)
        # self.custom_bg=(.5,.2,.1,1)
        # return self.custom_bg
    
    def add_category(self,text):
        if text.text =='':
            print('empty')
        else:
            now = datetime.now()
            self.screen_manager.get_screen('MainPage').ids.Main_page.clear_widgets()
            db.child('Users').child(self.user).child('Categories').child((text.text).lower()).child('info').set({'icon':str(self.selected_category)})
            db.child('Users').child(self.user).child('Categories').child((text.text).lower()).child('items').push({'Email':'abc@example.com','Password':'examplepassword','Hint':'example hint','Category':(text.text).lower(),'key':str(now)})
            Clock.schedule_once(lambda x: self.show_categories(),.5)
         
    def add_category_dialog(self):
        self.category_dialog = MDDialog(
                type="custom",
                content_cls=Category_content(),
                pos_hint={'center_y':.7 },
            )
        self.category_dialog.open()
        
    def edit_details_dialog(self,category,hint,email,password,key):
        self.edit_email=email
        self.edit_pass=password
        self.edit_hint=hint
        self.edit_category=category
        self.edit_key=key
        self.edit_dialog = MDDialog(
                type="custom",
                content_cls=Eidt_details(),
                pos_hint={'center_y':.7 },

                height= self.w[1]/4.2,
                radius=[20,],
                md_bg_color=self.theme_cls.bg_light,
            )
        self.edit_dialog.content_cls.ids.edit_email.text = self.edit_email
        self.edit_dialog.content_cls.ids.edit_hint.text = self.edit_hint
        self.edit_dialog.content_cls.ids.edit_pass.text = self.edit_pass
        self.edit_dialog.content_cls.ids.edit_key.text = self.edit_key
        self.edit_dialog.content_cls.ids.edit_category.text = self.edit_category
        self.edit_dialog.open()
        
    def add_details_dialog(self):
       
        self.add_credentials_dialog = MDDialog(
                type="custom",
                content_cls=Add_Credentials(),
                pos_hint={'center_y':.7 },
                height= self.w[1]/4.2,
                radius=[20,],
                md_bg_color=self.theme_cls.bg_light,
            )
        self.add_credentials_dialog.open()
        
    def update_details(self,edit_key,edit_category,edit_hint,edit_email,edit_pass):
              
        data  = {
            'Email':edit_email,
            'Password':edit_pass,
            'Hint':edit_hint,
           
        }
        details =db.child('Users').child(self.user).child('Categories').child(edit_category).child('items').get()
        for i in details.each():
            if i.val()['key']==edit_key:
                db.child('Users').child(self.user).child('Categories').child(edit_category).child('items').child(i.key()).update(data)
                break
        self.edit_dialog.dismiss()
        Clock.schedule_once(lambda x, val = edit_category:  self.refresh_details(val))

    def text_replace(self,text,limit):
        # print(text.text)
        limit +=1
        if len(text.text) == limit:
            text.text = text.text[:limit-1]
        else:
            pass

    def dismiss_category(self):
        self.category_dialog.dismiss()
        
    def delete_category(self,deleted_category):
        list_of_categories=db.child('Users').child(self.user).child('Categories').get()
        if len(list_of_categories.each())==1: 
            self.show_dialog('Warning',"At least one Category is required")
        else:
            self.screen_manager.get_screen('MainPage').ids.Main_page.clear_widgets()
            db.child('Users').child(self.user).child('Categories').child(deleted_category).remove()
            Clock.schedule_once(lambda x: self.show_categories())
        
    def detailsPage(self,val,category):
        self.screen_manager.get_screen('DetailsScreen').ids.details_title.text = category.upper()
        value = val
        self.screen_manager.current = 'DetailsScreen'
        self.screen_manager.get_screen('DetailsScreen').ids.details.clear_widgets()
        for i in value.values():
            card = MDCard(
                radius=[20,],
                padding=dp(20),
                size_hint_y=None,
                height=self.w[1]/4.5,
                orientation='vertical',
            )
            # items in box layout
            box_layout1 = MDBoxLayout(
                adaptive_height=True,
                size_hint_y=.3,
            )
            label1 = MDLabel(
                font_name='font/BlaakLightItalic_PERSONAL.ttf',
                text=i['Hint'],
                pos_hint={'top':1},
                theme_text_color='Custom',
                text_color=self.theme_cls.primary_color,
                adaptive_height=True,
            )
            icon_btn_edit = MDIconButton(
                ripple_scale=0,
                ripple_color=self.theme_cls.bg_light,
                icon='square-edit-outline',
                adaptive_height=True,
                pos_hint={'center_y':.8},
                on_press=lambda x,key=i['key'],category= i['Category'], hint= i['Hint'],email= i['Email'],password = i['Password']: self.edit_details_dialog(category,hint,email,password,key),
            )
            icon_btn_delete = MDIconButton(
                ripple_scale=0,
                ripple_color=self.theme_cls.bg_light,
                icon='delete-outline',
                adaptive_height=True,
                pos_hint={'center_y':.8},
                on_press=lambda x ,key=i['key'],category=i['Category']: self.delete_details(category,key),
            )
            
            box_layout1.add_widget(label1)
            box_layout1.add_widget(icon_btn_edit)
            box_layout1.add_widget(icon_btn_delete)
            
            #GridLayout
            
            grid_layout=MDGridLayout(
                cols=3,
            )
            email_icon = MDIcon(
                    icon='email',
                    size_hint_x=.15
            )
            email=MDLabel(
                font_name='font/BlaakLightItalic_PERSONAL.ttf',
                text=i['Email'],
            )
            copy_icon1 = MDIconButton(
                    ripple_scale=0,
                    ripple_color=self.theme_cls.bg_light,
                    icon='content-copy',
                    on_press=lambda x, val = i['Email']:self.snackbar_show(val)
                        )
            
            # for password
            grid_layout=MDGridLayout(
                cols=3,
            )
            pass_icon = MDIcon(
                    icon='key',
                    size_hint_x=.15
            )
            password=MDLabel(
                font_name='font/BlaakLightItalic_PERSONAL.ttf',
                text=i['Password'],
            )
            copy_icon2 = MDIconButton(
                    ripple_scale=0,
                    ripple_color=self.theme_cls.bg_light,
                    icon='content-copy',
                    on_press=lambda x, val = i['Password']:self.snackbar_show(val)
                        )
            
            grid_layout.add_widget(email_icon)
            grid_layout.add_widget(email)
            grid_layout.add_widget(copy_icon1)
            
            grid_layout.add_widget(pass_icon)
            grid_layout.add_widget(password)
            grid_layout.add_widget(copy_icon2)
            
            
            card.add_widget(box_layout1)
            card.add_widget(MDSeparator())
            card.add_widget(grid_layout)
            
            
            self.screen_manager.get_screen('DetailsScreen').ids.details.add_widget(
                card)
        
    def refresh_details(self,category):
        # self.screen_manager.get_screen('DetailsScreen').ids.details.clear_widgets()
        selected = db.child('Users').child(self.user).child('Categories').child(category).get()
        for i in selected.each():
            if i.key() =='items':
                # print(i.val())
                self.detailsPage(i.val(),category)
            
    def delete_details(self,category,key):
        selected = db.child('Users').child(self.user).child('Categories').child(category).child('items').get()
        if len(selected.each())==1:
            self.show_dialog('Warning',"At least one item is required")
        else:                
            for i in selected.each():
                if i.val()['key']==key:
                    db.child('Users').child(self.user).child('Categories').child(category).child('items').child(i.key()).remove()
                    self.refresh_details(category)
                    return
                
                
    def show_categories(self):
        self.screen_manager.get_screen('MainPage').ids.Main_page.clear_widgets()
        categ = db.child('Users').child(self.user).child('Categories').get()

        for i in categ.each():
            if i.val()['info']['icon'] =='Other':
                current_icon = 'heart'
            else:
                current_icon = i.val()['info']['icon']
                
            current_category = i.key()
            
            card = MDCard(
                        padding= ('10dp', '5dp', '10dp', '10dp'),
                        size_hint_y=None,
                        height=self.w[1]/9,
                        elevation=15,
                        radius=[20,],
                        )
            Inner_card = MDCard(
                size_hint_x=.8,
                elevation=0,
                md_bg_color=self.theme_cls.bg_light,
                on_press=lambda x ,value =i.val()['items'] :self.add_details(value),
            )
            
            Category_icon=ClickableMDIcon(
                icon=current_icon.lower(),
                font_size=sp(35),
                theme_text_color='Custom',
                text_color=self.theme_cls.primary_color,
                size_hint_x=.38,
            )
            Category_text=MDLabel(
               text=current_category.upper(),
               font_name=self.font,
            )
            Category_text.font_size=sp(15)
            Inner_card.add_widget(Category_icon)
            Inner_card.add_widget(Category_text)
            card.add_widget(Inner_card)
            
            
            delete_icon=ClickableMDIcon(
                icon='delete-outline',
                size_hint=(.11,.4),
                pos_hint= { 'center_y':.5 },
                font_size=sp(18),
                on_release=lambda x ,val = i.key():self.delete_category(val),
            )
            card.add_widget(delete_icon)
            # delete_icon=ClickableMDIcon(
            #             icon='delete-outline',
            #             pos_hint={'center_x':.9},
            #             size_hint=(.2,.1) ,
            #             theme_text_color='Custom',
            #             text_color=self.theme_cls.primary_color,
            #             on_release=lambda x ,val = i.key():self.delete_category(val),
            #             # adaptive_size=True,
                        
            # )
            # delete_icon.font_size='20sp'
            # self.category_icon=ClickableMDIcon(
            #             icon=current_icon.lower(),
            #             size_hint_y=.5,
            #             font_size='64sp',
            #             halign='center',
            #             pos_hint={'center_y':.5},
            #             theme_text_color='Custom',
            #             text_color=self.theme_cls.primary_color,
            #             on_press=lambda x ,value =i.val()['items'] :self.add_details(value) ,
                        
            # )
            # self.category_icon.font_size='64sp'
            # # self.category_icon.bind(on_press=lambda x: self.test())
            # separator=MDSeparator()
            # category_text=MDLabel(
            #     font_name='font/BlaakLightItalic_PERSONAL.ttf',
            #             size_hint_y=.2,
            #             text=current_category.upper(),
            #             pos_hint={'center_y':.5},
            #             theme_text_color='Custom',
            #             text_color=self.theme_cls.primary_color,
            #             halign='center',
            # )
            # category_text.font_size = '15sp'
            # card.add_widget(delete_icon)
            # card.add_widget(self.category_icon)
            # card.add_widget(separator)
            # card.add_widget(category_text)
            self.screen_manager.get_screen('MainPage').ids.Main_page.add_widget(card)
            
            
    def snackbar_show(self,value):
        Clipboard.copy(value)
        self.snackbar = Snackbar(
            text='Copied '+value,
            duration=1,
            )
        self.snackbar.open()
        

    def update_kv_files(self,text):
        
        with open(self.path_to_kv_file,"w+") as kv_file:
            kv_file.write(text)
  
    def change_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"



    def show_dialog(self, title, text):
        title = title
        text = text
        cancel_btn_username_dialouge = MDFlatButton(
            text="Okay", on_release=self.close_dialog)
        self.dialog = MDDialog(title=title, text=text, size_hint=(
            0.7, 0.2), buttons=[cancel_btn_username_dialouge])
        self.dialog.open()

    def close_dialog(self, obj):
            self.dialog.dismiss()
            
    def close_profile_dialog(self, obj):
            self.profile_dialouge.dismiss()
        
if __name__=='__main__':
    Main().run()