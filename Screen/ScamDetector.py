import pytesseract
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.camera import Camera
from datetime import datetime
from PIL import Image
from pathlib import Path
from spellchecker import SpellChecker
import re

# Set Tesseract path if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
spellChecker = SpellChecker()

class ScamDetectorApp(App):
    def build(self):
        # Hardcoded scam datasets
        self.scamEmails = {
            "support@paypal-fraud.com",
            "lottery@netflix-payments.com",
            "account@amazon-secure.com"
        }

        self.scamDomains = {
            "paypal-fraud.com",
            "netflix-payments.com",
            "amazon-secure.com"
        }

        self.scamPhones = {
            "18005551234",
            "18887776666",
            "1234567890"
        }

        self.scamUrls = {
            "http://netflix-payments.com/update",
            "https://paypal-secure-alert.com/login",
            "http://free-lottery-win.ru",
            "https://security.hsbc.confirm-added-payee.com"
        }

        self.mainLayout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.selectButton = Button(text='Select Image', size_hint=(1, 0.1))
        self.selectButton.bind(on_release=self.openFileChooser)
        self.mainLayout.add_widget(self.selectButton)

        self.cameraButton = Button(text='Take Photo', size_hint=(1, 0.1))
        self.cameraButton.bind(on_release=self.openCamera)
        self.mainLayout.add_widget(self.cameraButton)

        self.resultLabel = Label(
            text='Text will appear here...',
            size_hint=(1, None),
            halign='left',
            valign='top',
            markup=True
        )
        self.resultLabel.bind(texture_size=self.adjustLabelHeight)

        scrollView = ScrollView()
        scrollView.add_widget(self.resultLabel)
        self.mainLayout.add_widget(scrollView)

        return self.mainLayout

    def adjustLabelHeight(self, instance, value):
        self.resultLabel.height = self.resultLabel.texture_size[1]
        self.resultLabel.text_size = (self.resultLabel.width, None)

    def openFileChooser(self, instance):
        contentLayout = BoxLayout(orientation='vertical')
        defaultPath = str(Path.home() / "Downloads")
        fileChooser = FileChooserIconView(path=defaultPath)
        contentLayout.add_widget(fileChooser)
        selectButton = Button(text="Select", size_hint=(1, 0.1))
        contentLayout.add_widget(selectButton)
        filePopup = Popup(title="Choose an image", content=contentLayout, size_hint=(0.9, 0.9))

        def onSelect(instance):
            if fileChooser.selection:
                filePopup.dismiss()
                self.processImage(fileChooser.selection[0])

        selectButton.bind(on_release=onSelect)
        filePopup.open()

    def openCamera(self, instance):
        try:
            self.camera = Camera(index=0, play=True, resolution=(640, 480))
            if not self.camera._camera:
                raise RuntimeError("No camera found or camera backend failed to load.")
            captureButton = Button(text="Capture", size_hint=(1, 0.15))
            layout = BoxLayout(orientation='vertical')
            layout.add_widget(self.camera)
            layout.add_widget(captureButton)
            self.cameraPopup = Popup(title="Take a Photo", content=layout, size_hint=(0.9, 0.9))
            self.cameraPopup.open()
            captureButton.bind(on_release=self.capturePhoto)
        except Exception as e:
            errorPopup = Popup(
                title="Camera Error",
                content=Label(text=f"[b]Error:[/b] Camera not found.", markup=True),
                size_hint=(0.8, 0.3)
            )
            errorPopup.open()

    def capturePhoto(self, instance):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{timestamp}.png"
        self.camera.export_to_png(filename)
        self.cameraPopup.dismiss()
        self.processImage(filename)

    def processImage(self, filePath):
        try:
            image = Image.open(filePath)
            text = pytesseract.image_to_string(image)
            linkCheckText = text.replace("\n", "")
            spellingCheckText = re.sub(r'[^a-zA-Z\s]', '', text)
            emailCheckText = text.replace("\n", "")

            misspelledWords = spellChecker.unknown(spellingCheckText.split())
            pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
            links = re.findall(pattern, linkCheckText)
            emailPattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
            emails = re.findall(emailPattern, emailCheckText)
            phonePattern = r'\b(?:\+?(\d{1,3}))?[-.\s(]*(\d{3})[-.\s)]*(\d{3})[-.\s]*(\d{4})\b'
            rawNumbers = re.findall(phonePattern, text)
            phones = [''.join(number) for number in rawNumbers]

            scamKeyWords = [
                "verify your account", "click here", "urgent", "suspended", "winner",
                "update your payment", "limited time", "claim now", "bank details",
                "free", "offer expires", "password", "SSN", "credit card", "action", "required",
            ]
            foundKeywords = [kw for kw in scamKeyWords if kw in text.lower()]

            result = text if text.strip() else "[No text found]"

            # --- Risk scoring system ---
            riskOdds = 0
            certainRisk = False

            # Link check using hardcoded scam URLs and domains
            if links:
                for link in links:
                    domain = re.sub(r'^https?://(www\.)?', '', link).split('/')[0].lower()
                    domainMatch = domain in self.scamDomains

                    if link.lower() in self.scamUrls:
                        certainRisk = True
                        result += f"\n\n[color=ff0000][b]Scam URL Match:[/b][/color] {link}"
                    elif domainMatch:
                        certainRisk = True
                        result += f"\n\n[color=ff0000][b]Scam domain match:[/b][/color] {domain}"
                    else:
                        result += f"\n\n[i]Link safe:[/i] {link}"
            else:
                result += "\n\n[i]No links found[/i]"

            # Email check
            if emails:
                result += "\n\n[b]Emails found:[/b]\n" + "\n".join(emails)

                scamEmailMatches = []
                for email in emails:
                    if email.lower() in self.scamEmails:
                        scamEmailMatches.append(email)
                        certainRisk = True

                if scamEmailMatches:
                    result += f"\n\n[color=ff0000][b]Scam Email Matches:[/b][/color]"
                    result += "\n" + "\n".join(scamEmailMatches)
                else:
                    result += "\n[i]No known scam email matches[/i]"
            else:
                result += "\n\n[i]No emails found[/i]"

            # Phone number check
            if phones:
                result += "\n\n[b]Phone numbers found:[/b]\n" + "\n".join(phones)

                scamPhoneMatches = []
                for phone in phones:
                    cleanPhone = re.sub(r'\D', '', phone)
                    if cleanPhone in self.scamPhones:
                        scamPhoneMatches.append(phone)
                        certainRisk = True

                if scamPhoneMatches:
                    result += f"\n\n[color=ff0000][b]Scam Phone Matches:[/b][/color]"
                    result += "\n" + "\n".join(scamPhoneMatches)
                else:
                    result += "\n[i]No known scam phone matches[/i]"
            else:
                result += "\n\n[i]No phone numbers found[/i]"

            # Misspelled words
            if misspelledWords:
                result += "\n\n[b]Misspelled words:[/b]\n" + ", ".join(sorted(misspelledWords))
                if len(misspelledWords) > 6:
                    riskOdds += 25
                elif len(misspelledWords) > 3:
                    riskOdds += 15
            else:
                result += "\n\n[i]No spelling errors detected[/i]"

            # Scam keywords
            if foundKeywords:
                result += "\n\n[b]Scam keywords found:[/b]\n" + "\n".join(foundKeywords)
                riskOdds += 10 * len(foundKeywords)
            else:
                result += "\n\n[i]No scam keywords found[/i]"

            if certainRisk:
                riskLabel = "[b][color=ff0000]High Risk[/color][/b] — Scam indicators confirmed (100%)"
            else:
                riskOdds = min(riskOdds, 95)
                if riskOdds >= 70:
                    riskLabel = f"[b][color=ff0000]High Risk[/color][/b] — Estimated risk: {riskOdds}%"
                elif riskOdds >= 40:
                    riskLabel = f"[b][color=ffaa00]Medium Risk[/color][/b] — Estimated risk: {riskOdds}%"
                else:
                    riskLabel = f"[b][color=00aa00]Low Risk[/color][/b] — Estimated risk: {riskOdds}%"

            self.resultLabel.text = f"{riskLabel}\n\n{result}"

        except Exception as error:
            self.resultLabel.text = f"[color=ff0000]Error: {error}[/color]"
            


if __name__ == '__main__':
    ScamDetectorApp().run()