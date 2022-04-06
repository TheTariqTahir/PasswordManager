from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp, sp
# import requests
# from kivymd.utils import asynckivy
from kivymd.uix.card import MDCard, MDSeparator
from kivy.animation import Animation
from kivymd.uix.snackbar import Snackbar
from kivy.factory import Factory
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton,MDIconButton
from kivy.clock import Clock
# from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.label import MDLabel, MDIcon
# from kivymd.uix.picker import MDDatePicker
# from kivymd.uix.list import TwoLineIconListItem,TwoLineListItem
# from kivymd.uix.label import MDLabel
from kivymd.utils.fitimage import FitImage
from kivy.core.window import Window







class MainPage(Screen):
    pass

class ProfileScreen(Screen):
    pass

class DetailsScreen(Screen):
    pass

class ShowPassword(Screen):
    pass


sm = ScreenManager()


sm.add_widget(MainPage(name='MainPage'))
sm.add_widget(ProfileScreen(name='ProfileScreen'))
sm.add_widget(DetailsScreen(name='DetailsScreen'))
sm.add_widget(ShowPassword(name='ShowPassword'))





class Main(MDApp):
    path_to_kv_file='kv_file.kv'
    
    def build(self):
        self.w= Window.size = 460,700
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = "A400"
        self.theme_cls.theme_style = "Light"
        # self.theme_cls.theme_style = "Dark"
        self.custom_name = 'Company Name'


        # text_file = open('hotreloader.kv','r')
        # KV= text_file.read()
        # self.builder = Builder.load_string(KV)

        
        self.builder = Builder.load_file('kv_file.kv')
        self.screen_manager = self.builder.ids.front_layer.children[0].ids.new_screen_manger
        self.show_categories()
        return self.builder
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Clock.schedule_once(self.myFunc,3)

  
    def show_categories(self):
        card = MDCard(
            md_bg_color=self.theme_cls.bg_light,
            size_hint= (.5,None),
            elevation=dp(15),
            radius=dp(20),
            height=self.w[1]/6.5,
            orientation= 'vertical',
            padding= ('20dp', '10dp', '20dp', '20dp'),
        )
        
        icon= MDIconButton(
            icon='facebook',
            # halign='center',
            
            # # font_style='H6',
            user_font_size=sp(64),
            pos_hint= {'center_x': 0.5,'center_y': 0.5},
            theme_text_color='Custom',
            text_color=self.theme_cls.primary_dark,
        )
        separator = MDSeparator()
        box_layout=MDBoxLayout(orientation= 'vertical',spacing=dp(10))
        label= MDLabel(
            pos_hint={'center_y':.1},
            size_hint= (1,.1),
            text='Facebook',
            halign='center',
            font_style='H6',
            theme_text_color='Custom',
            text_color=self.theme_cls.primary_dark,
        )
        

        box_layout.add_widget(icon)
        box_layout.add_widget(separator)
        box_layout.add_widget(label)

        card.add_widget(box_layout)
        print(self.screen_manager.get_screen('MainPage').ids.mainPageCard.add_widget(card))
            

    def snackbar_show(self,value):
        
        self.snackbar = Snackbar(
            text=value,
            duration=2,
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
        self.dialog = MDDialog(title=text, text=text, size_hint=(
            0.7, 0.2), buttons=[cancel_btn_username_dialouge])
        self.dialog.open()

    def close_dialog(self, obj):
            self.dialog.dismiss()
            self.profile_dialouge.dismiss()
            
    def close_profile_dialog(self, obj):
            self.profile_dialouge.dismiss()
        
if __name__=='__main__':
    Main().run()