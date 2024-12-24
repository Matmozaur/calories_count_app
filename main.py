from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from plyer import tts
import speech_recognition as sr
import re
from word2number import w2n

class SpeechToTextApp(App):
    def build(self):
        self.recognizer = sr.Recognizer()
        self.main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.label = Label(text="Press a button to begin")
        self.main_layout.add_widget(self.label)

        self.btn1 = Button(text="Provide calories and protein", size_hint=(1, 0.2))
        self.btn1.bind(on_press=self.listen_to_speech)
        self.main_layout.add_widget(self.btn1)

        self.btn2 = Button(text="Provide exercise, weight, and repetitions", size_hint=(1, 0.2))
        self.btn2.bind(on_press=self.listen_to_speech)
        self.main_layout.add_widget(self.btn2)

        return self.main_layout


    def listen_to_speech(self, instance):
        self.label.text = "Listening..."
        try:
            with sr.Microphone() as source:
                # Adjust microphone settings
                self.recognizer.pause_threshold = 1.5

                audio = self.recognizer.listen(source, phrase_time_limit=15)

                self.label.text = "Processing..."
                text = self.recognizer.recognize_google(audio)

                res = self.format_text(text)
                self.show_data_options(res)

        except sr.UnknownValueError:
            self.label.text = "Could not understand audio"
        except sr.RequestError as e:
            self.label.text = f"Request error: {e}"
        except OSError as e:
            self.label.text = f"OSError: {e}"

    def format_text(self, text):
        print(text, flush=True)

        res = {'Calories': 0, 'Proteins': 0}

        last = None
        for word in text.split(" "):
            print(last, flush=True)
            print(word, flush=True)
            if 'cal' in word.lower():
                res['Calories'] = w2n.word_to_num(last.replace(",", ""))
            elif 'pro' in word.lower():
                res['Proteins'] = w2n.word_to_num(last.replace(",", ""))
            last = word

        return res

    def show_data_options(self, text):
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        message = Label(text=f"Do you want to send this data: {text} or input manually?")
        popup_layout.add_widget(message)

        button_layout = BoxLayout(size_hint_y=0.3)

        send_button = Button(text="Send Data")
        send_button.bind(on_press=lambda instance: self.close_popup())
        button_layout.add_widget(send_button)

        manual_button = Button(text="Input Manually")
        manual_button.bind(on_press=lambda instance: self.input_manually())
        button_layout.add_widget(manual_button)

        popup_layout.add_widget(button_layout)

        self.popup = Popup(title="Choose an Option", content=popup_layout, size_hint=(0.8, 0.5))
        self.popup.open()

    def close_popup(self):
        self.popup.dismiss()

    def input_manually(self):
        self.popup.dismiss()
        
        self.main_layout.clear_widgets()

        self.label = Label(text="Input two numbers:")
        self.main_layout.add_widget(self.label)

        self.input1 = TextInput(hint_text="Enter first number", multiline=False)
        self.main_layout.add_widget(self.input1)

        self.input2 = TextInput(hint_text="Enter second number", multiline=False)
        self.main_layout.add_widget(self.input2)

        submit_button = Button(text="Submit", size_hint=(1, 0.2))
        submit_button.bind(on_press=self.submit_manual_input)
        self.main_layout.add_widget(submit_button)

    def submit_manual_input(self, instance):
        num1 = self.input1.text
        num2 = self.input2.text
        self.label.text = f"You entered: {num1} and {num2}"

if __name__ == "__main__":
    SpeechToTextApp().run()
