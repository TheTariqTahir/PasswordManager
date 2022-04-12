from kivy.lang import Builder
from datetime import datetime
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp, sp
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton,MDIconButton

from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivymd.uix.label import MDLabel, MDIcon
from kivy.core.window import Window



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



class MainPage(Screen):
    pass

class ProfileScreen(Screen):
    pass

class DetailsScreen(Screen):
    pass

class ShowPassword(Screen):
    pass


class Category_content(MDBoxLayout):
    # def __init__(self):
    pass

class Eidt_details(MDBoxLayout):
    pass

class Add_Credentials(MDBoxLayout):
    pass
    


sm = ScreenManager()


sm.add_widget(MainPage(name='MainPage'))
sm.add_widget(ProfileScreen(name='ProfileScreen'))
sm.add_widget(DetailsScreen(name='DetailsScreen'))
sm.add_widget(ShowPassword(name='ShowPassword'))





class Main(MDApp):
    path_to_kv_file='kv_file.kv'
    
    def build(self):
        # self.w= Window.size 
        self.w= Window.size = 390,650
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "A700"
        self.theme_cls.theme_style = "Light"

        self.text_size= (self.w[0]+self.w[1])/2

        # text_file = open('hotreloader.kv','r')
# KV= text_file.read()
        # self.builder = Builder.load_string(KV)
        self.builder = Builder.load_file('kv_file.kv')
        
        self.selected_category=''
        self.selected_details={}
        self.user = 'User1'
        
        self.details_page_category=''
        
        self.edit_email=''
        self.edit_pass=''
        self.edit_hint=''
        self.edit_category=''
        self.key=''
        
        
        self.screen_manager = self.builder.ids.front_layer.children[0].ids.new_screen_manger
        Clock.schedule_once(lambda x: self.show_categories())
        return self.builder

    def run_async(self):
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
        self.refresh_details(category)
    
    
    
    def add_category(self,text):
        now = datetime.now()
        self.screen_manager.get_screen('MainPage').ids.mainPageCard.clear_widgets()
        db.child('Users').child(self.user).child('Categories').child((text.text).lower()).child('info').set({'icon':str(self.selected_category)})
        db.child('Users').child(self.user).child('Categories').child((text.text).lower()).child('items').push({'Email':'abc@example.com','Password':'examplepassword','Hint':'example hint','Category':(text.text).lower(),'key':str(now)})
        Clock.schedule_once(lambda x: self.show_categories(),.5)
         
    def add_category_dialog(self):
        self.category_dialog = MDDialog(
                type="custom",
                content_cls=Category_content(),
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
            self.screen_manager.get_screen('MainPage').ids.mainPageCard.clear_widgets()
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
        self.screen_manager.get_screen('MainPage').ids.mainPageCard.clear_widgets()
        categ = db.child('Users').child(self.user).child('Categories').get()

        for i in categ.each():
            if i.val()['info']['icon'] =='Other':
                current_icon = 'heart'
            else:
                current_icon = i.val()['info']['icon']
                
            current_category = i.key()
            
            card = MDCard(
                md_bg_color=self.theme_cls.bg_light,
                size_hint= (.5,None),
                height=self.w[1]/7,
                elevation=dp(2),
                radius=dp(20),
                orientation= 'vertical',
                padding= ('20dp', '10dp', '20dp', '20dp'),
                
            )

            delete_float = FloatLayout(size_hint_y=.1)
            delete_icon = MDIconButton(
                                ripple_scale=0,
                                ripple_color=self.theme_cls.bg_light,
                                icon='delete-outline',
                                user_font_size='20sp',
                                pos_hint={'center_y':.5,'center_x':.95},
                                on_release=lambda x ,val = i.key():self.delete_category(val),
                                theme_text_color='Custom',
                                text_color=self.theme_cls.primary_color,
                            )
                            
            delete_float.add_widget(delete_icon)
            
            anchor = AnchorLayout()
            icon= MDIconButton(

                icon=current_icon.lower(),
                ripple_scale=0,
                ripple_color=self.theme_cls.bg_light,
                user_font_size=sp(38),
                pos_hint= {'center_x': 0.5,'center_y': .4},
                theme_text_color='Custom',
                text_color=self.theme_cls.primary_color,
                on_press=lambda x ,value =i.val()['items'] :self.add_details(value) ,
                
            )
            anchor.add_widget(icon)
            
            separator = MDSeparator()
            box_layout=MDBoxLayout(orientation= 'vertical',spacing=dp(10))

            main_anchor_layout=AnchorLayout()
            label_anchor_layout=AnchorLayout(anchor_x='center',anchor_y='center')
            label= MDLabel(
                text=current_category.upper(),
                halign='center',
                font_style='Button',
                # font_size=sp(50),
                size_hint_x=1,
                theme_text_color='Custom',
                text_color=self.theme_cls.primary_color,
            )
            label_anchor_layout.add_widget(label)

            main_anchor_layout.add_widget(label_anchor_layout)
            
            box_layout.add_widget(delete_float)
            box_layout.add_widget(anchor)
           
            box_layout.add_widget(separator)


            new_Box_layout=MDBoxLayout(size_hint=(1,.1))
            # new_Box_layout.add_widget(delete_icon)
            # box_layout.add_widget(label)

            new_Box_layout.add_widget(main_anchor_layout)
            # new_Box_layout.add_widget(delete_icon)
            
            
            box_layout.add_widget(new_Box_layout)
            card.add_widget(box_layout)
            
            self.screen_manager.get_screen('MainPage').ids.mainPageCard.add_widget(card)
            
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