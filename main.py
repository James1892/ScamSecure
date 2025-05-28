from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from Screen.Home import HomePage
from Screen.ReportHub import ReportPage
from Screen.educationHub import EducationPage

from Screen.Quiz import quizPage

class HackaburryApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        sm = ScreenManager()
        sm.add_widget(HomePage(name="home"))
        sm.add_widget(ReportPage(name="reporthub"))
        sm.add_widget(EducationPage(name="educationhub"))
        sm.add_widget(quizPage(name='quiz')) 

        return sm


if __name__ == "__main__":
    HackaburryApp().run()
