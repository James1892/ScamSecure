from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.properties import StringProperty
import random
import os


# Ensure the correct path to Home.kv
Builder.load_file(os.path.join(os.path.dirname(__file__), "Home.kv"))

class HomePage(MDScreen):
    tip_text = StringProperty()

    def on_enter(self):
        tips = [
    "Be cautious of messages urging immediate action; scammers create a sense of urgency.",
    "Never send money or gift cards to someone you haven't met in person.",
    "Verify unexpected messages or requests through a separate, trusted communication method.",
    "Don’t trust caller ID scammers can spoof phone numbers.",
    "Be sceptical of 'too good to be true' offers or prizes.",
    "Install and regularly update antivirus and anti-malware software.",
    "Be cautious when sharing personal information on social media.",
    "Check reviews and verify legitimacy before purchasing from unknown websites.",
    "Report suspicious activity to authorities or relevant platforms.",
    "Educate friends and family, especially the elderly, about common scam tactics."
        ]
        self.tip_text = random.choice(tips)

