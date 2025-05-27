from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.app import App
import os

Builder.load_file(os.path.join(os.path.dirname(__file__), "ReportHub.kv"))

class ReportPage(MDScreen):
    def return_home(self, *args):
        app = App.get_running_app()
        app.root.current = 'home'

