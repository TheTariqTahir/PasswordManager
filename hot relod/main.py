from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.metrics import dp, sp
# import requests

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
# from kivymd.uix.list import ThreeLineListItem
# from kivymd.uix.label import MDLabel
# from kivymd.uix.menu import MDDropdownMenut
# from kivymd.uix.picker import MDDatePicker
# from kivymd.uix.list import TwoLineIconListItem,TwoLineListItem
# from kivymd.uix.label import MDLabel

from kivymd.uix.behaviors import (
    FakeCircularElevationBehavior,
)

from kivy.core.window import Window
Window.size = 360,600


class CircleCard(
    FakeCircularElevationBehavior,
    MDCard,
):
    pass
class WelcomeScreen(Screen):
    pass


class MainPage(Screen):
    pass

class ProductsPage(Screen):
    pass


class AboutPage(Screen):
    pass


class ProfilePage(Screen):
    pass


sm = ScreenManager()

sm.add_widget(WelcomeScreen(name='WelcomeScreen'))
sm.add_widget(MainPage(name='MainPage'))
sm.add_widget(AboutPage(name='AboutPage'))
sm.add_widget(ProfilePage(name='ProfilePage'))
sm.add_widget(ProductsPage(name='ProductsPage'))



class Main(MDApp):
    path_to_kv_file='kv_file.kv'
    
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.theme_style = "Light"
        # self.theme_cls.theme_style = "Dark"
        self.custom_name = 'Company Name'


        text_file = open('hotreloader.kv','r')
        KV= text_file.read()
        self.builder = Builder.load_string(KV)
        
        # self.builder = Builder.load_file('kv_file.kv')

        return self.builder


    def change_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"


    def update_kv_files(self,text):
        
        with open(self.path_to_kv_file,"w+") as kv_file:
            kv_file.write(text)
    def toggle_nav(self):
            self.root.ids.nav_drawer.set_state('toggle')




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
        
if __name__=='__main__':
    Main().run()