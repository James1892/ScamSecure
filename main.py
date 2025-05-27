import Screen.Config as config
config.apply_window_size()

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from Screen.Home import HomePage
from Screen.ReportHub import ReportPage

class HackaburryApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        sm = ScreenManager()
        sm.add_widget(HomePage(name="home"))
        sm.add_widget(ReportPage(name="reporthub"))
        return sm


if __name__ == "__main__":
    HackaburryApp().run()
