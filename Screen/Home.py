from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import os

# Ensure the correct path to Home.kv
Builder.load_file(os.path.join(os.path.dirname(__file__), "Home.kv"))


class HomePage(MDScreen):
    pass
