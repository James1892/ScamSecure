from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.app import App
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import os
import random

Builder.load_file(os.path.join(os.path.dirname(__file__), "Quiz.kv"))

class quizPage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.quiz_data = [
            {
                "question": "You receive a phone call from someone claiming to be from Microsoft. They say your computer has been hacked and ask you to install remote access software so they can 'fix it.'",
                "answer": "Computer Software Service Fraud"
            },
            {
                "question": "A stranger offers to help when your card gets stuck in a cash machine. After you leave, they retrieve your card and use the PIN you entered to withdraw money.",
                "answer": "Banking and Card Fraud – Cash Machines"
            },
            {
                "question": "You are contacted by someone on a dating app who quickly declares their love, then says they are stranded overseas and need money for a sick child.",
                "answer": "Romance and Dating Fraud"
            },
            {
                "question": "You get a letter saying you've won £10,000 in a prize draw, but to claim it, you must send £30 to cover processing fees.",
                "answer": "Scam Mail"
            },
            {
                "question": "You buy what looks like a discounted luxury holiday villa online. When you arrive, the property doesn't exist.",
                "answer": "Holiday Fraud"
            },
            {
                "question": "A caller claims to be from your bank and says there's been fraudulent activity. They urge you to transfer your money to a 'safe account.'",
                "answer": "Authorised Push Payment (APP) Fraud"
            },
            {
                "question": "Someone knocks on your door saying your roof is damaged and offers to repair it for £400 cash. After you pay, they leave and never come back.",
                "answer": "Door-to-Door Fraud"
            },
            {
                "question": "You receive an email telling you that you've inherited money from a distant relative. To access it, you must first pay a legal release fee.",
                "answer": "Advance Fee Fraud"
            },
            {
                "question": "A company contacts you with an exciting opportunity to invest in a rare gemstone business, promising high returns. You send money and never hear from them again.",
                "answer": "Investment Fraud"
            },
            {
                "question": "You buy a concert ticket from someone on social media. On the day of the event, the ticket turns out to be fake.",
                "answer": "Ticketing Fraud"
            },
            {
                "question": "Your HR department receives an email that appears to be from a senior manager requesting a large payment to a new supplier. After sending it, they realise the email was fake.",
                "answer": "Payment Fraud"
            },
            {
                "question": "Someone calls claiming to be a police officer investigating fraud. You're told to withdraw £2,000 and hand it to a courier for examination.",
                "answer": "Courier Fraud"
            },
            {
                "question": "You start getting bills for a phone contract and credit cards you never applied for. After checking, you find out someone used your name and details.",
                "answer": "Identity Fraud"
            },
            {
                "question": "You're offered a remote job but are told you must pay £50 upfront for training and equipment. Once you pay, the company disappears.",
                "answer": "Recruitment Fraud"
            },
            {
                "question": "You see an advert online for a brand-new smartphone at a great price. The seller asks for a direct bank transfer. After payment, you never receive the phone.",
                "answer": "Online Shopping and Auction Site Fraud"
            },
            {
                "question": "A person approaches you claiming you qualify for a government grant. But to receive it, you must first pay a processing fee. After you pay, they disappear.",
                "answer": "Advance Fee Fraud"
            },
            {
                "question": "You get an email appearing to be from HMRC, saying you're owed a tax refund. It asks you to input your bank details. Later, money is withdrawn from your account.",
                "answer": "Authorised Push Payment (APP) Fraud"
            },
            {
                "question": "Your internet stops working. You get a call from someone claiming to be from your provider, who asks you to install a program so they can fix the issue. Afterwards, you're charged and your files are missing.",
                "answer": "Computer Software Service Fraud"
            },
            {
                "question": "A friend recommends a business offering huge returns on cryptocurrency investments. You invest £3,000, then the company stops responding.",
                "answer": "Investment Fraud"
            },
            {
                "question": "You pay for two airline tickets through a third-party website. When you arrive at the airport, the airline has no record of your booking.",
                "answer": "Ticketing Fraud"
            }
        ]
        
        self.current_question_index = 0
        self.selected_answer = None
        self.score = 0
        self.current_question_data = None
        self.wrong_answers = []
        
        # Select 10 random questions for the quiz
        self.selected_questions = random.sample(self.quiz_data, 10)
        
        # Schedule the initialization after the screen is built
        Clock.schedule_once(self.initialize_quiz, 0.1)
    
    def initialize_quiz(self, dt):
        """Initialize the quiz when the screen is ready"""
        self.load_next_question()
    
    def generate_wrong_answers(self, correct_answer):
        """Generate 3 wrong answers from other questions"""
        all_answers = [q["answer"] for q in self.quiz_data]
        wrong_answers = [ans for ans in all_answers if ans != correct_answer]
        return random.sample(wrong_answers, min(3, len(wrong_answers)))
    
    def load_next_question(self):
        """Load the next question and generate answer options"""
        if self.current_question_index < len(self.selected_questions):
            self.current_question_data = self.selected_questions[self.current_question_index]
            
            # Update question text
            self.ids.question_label.text = self.current_question_data["question"]
            
            # Generate answer options
            correct_answer = self.current_question_data["answer"]
            wrong_answers = self.generate_wrong_answers(correct_answer)
            
            # Create list of all options and shuffle
            all_options = [correct_answer] + wrong_answers
            random.shuffle(all_options)
            
            # Update button texts
            self.ids.option_a.text = f"A. {all_options[0]}"
            self.ids.option_b.text = f"B. {all_options[1]}"
            self.ids.option_c.text = f"C. {all_options[2]}"
            self.ids.option_d.text = f"D. {all_options[3]}"
            
            # Store the correct option letter
            self.correct_option = chr(65 + all_options.index(correct_answer))  # A, B, C, or D
            
            # Reset selection
            self.selected_answer = None
            self.reset_button_colors()
            self.ids.submit_button.disabled = True
            
            # Update progress
            progress = f"Question {self.current_question_index + 1} of {len(self.selected_questions)}"
            self.ids.top_app_bar.title = progress
        else:
            self.show_final_score()
    
    def select_answer(self, option):
        """Handle answer selection"""
        self.selected_answer = option
        self.reset_button_colors()
        
        # Highlight selected button
        selected_color = [41/255, 128/255, 185/255, 1]  # Blue color for selected
        if option == "A":
            self.ids.option_a.md_bg_color = selected_color
        elif option == "B":
            self.ids.option_b.md_bg_color = selected_color
        elif option == "C":
            self.ids.option_c.md_bg_color = selected_color
        elif option == "D":
            self.ids.option_d.md_bg_color = selected_color
        
        # Enable submit button
        self.ids.submit_button.disabled = False
    
    def reset_button_colors(self):
        """Reset all button colors to default"""
        default_color = [52/255, 73/255, 94/255, 1]
        self.ids.option_a.md_bg_color = default_color
        self.ids.option_b.md_bg_color = default_color
        self.ids.option_c.md_bg_color = default_color
        self.ids.option_d.md_bg_color = default_color
    
    def submit_answer(self):
        """Process the submitted answer"""
        if self.selected_answer:
            # Check if answer is correct
            if self.selected_answer == self.correct_option:
                self.score += 1
                self.show_feedback("Correct!", True)
            else:
                correct_answer = self.current_question_data["answer"]
                self.show_feedback(f"Incorrect!\nThe correct answer was:\n{correct_answer}", False)
            
            # Move to next question after a delay
            Clock.schedule_once(lambda dt: self.next_question(), 2)
    
    def show_feedback(self, message, is_correct):
        """Show feedback dialog"""
        color = [46/255, 204/255, 113/255, 1] if is_correct else [231/255, 76/255, 60/255, 1]
        
        # You can implement a custom dialog here or just update button colors
        if is_correct:
            # Green for correct
            if self.selected_answer == "A":
                self.ids.option_a.md_bg_color = [46/255, 204/255, 113/255, 1]
            elif self.selected_answer == "B":
                self.ids.option_b.md_bg_color = [46/255, 204/255, 113/255, 1]
            elif self.selected_answer == "C":
                self.ids.option_c.md_bg_color = [46/255, 204/255, 113/255, 1]
            elif self.selected_answer == "D":
                self.ids.option_d.md_bg_color = [46/255, 204/255, 113/255, 1]
        else:
            # Red for incorrect, green for correct answer
            if self.selected_answer == "A":
                self.ids.option_a.md_bg_color = [231/255, 76/255, 60/255, 1]
            elif self.selected_answer == "B":
                self.ids.option_b.md_bg_color = [231/255, 76/255, 60/255, 1]
            elif self.selected_answer == "C":
                self.ids.option_c.md_bg_color = [231/255, 76/255, 60/255, 1]
            elif self.selected_answer == "D":
                self.ids.option_d.md_bg_color = [231/255, 76/255, 60/255, 1]
            
            # Highlight correct answer in green
            if self.correct_option == "A":
                self.ids.option_a.md_bg_color = [46/255, 204/255, 113/255, 1]
            elif self.correct_option == "B":
                self.ids.option_b.md_bg_color = [46/255, 204/255, 113/255, 1]
            elif self.correct_option == "C":
                self.ids.option_c.md_bg_color = [46/255, 204/255, 113/255, 1]
            elif self.correct_option == "D":
                self.ids.option_d.md_bg_color = [46/255, 204/255, 113/255, 1]
    
    def next_question(self):
        """Move to the next question"""
        self.current_question_index += 1
        self.load_next_question()
    
    def show_final_score(self):
        """Show the final score dialog"""
        percentage = (self.score / len(self.selected_questions)) * 100
        
        dialog = MDDialog(
            title="Quiz Complete!",
            text=f"Your Score: {self.score}/{len(self.selected_questions)}\nPercentage: {percentage:.1f}%",
            buttons=[
                MDFlatButton(
                    text="RESTART",
                    on_release=lambda x: self.restart_quiz(dialog),
                ),
                MDFlatButton(
                    text="HOME",
                    on_release=lambda x: self.go_home(dialog),
                ),
            ],
        )
        dialog.open()
    
    def restart_quiz(self, dialog):
        """Restart the quiz"""
        dialog.dismiss()
        self.current_question_index = 0
        self.score = 0
        self.selected_answer = None
        self.selected_questions = random.sample(self.quiz_data, 10)  # Select new random 10 questions
        self.load_next_question()
    
    def go_home(self, dialog):
        """Return to home screen"""
        dialog.dismiss()
        self.return_home()
    
    def return_home(self, *args):
        """Return to home screen"""
        app = App.get_running_app()
        app.root.current = 'home'