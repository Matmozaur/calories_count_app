from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from plyer import tts
import speech_recognition as sr


class SpeechToTextApp(App):
    def build(self):
        self.recognizer = sr.Recognizer()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.label = Label(text="Press the button and speak")
        layout.add_widget(self.label)

        self.btn = Button(text="Start Listening", size_hint=(1, 0.2))
        self.btn.bind(on_press=self.listen_to_speech)
        layout.add_widget(self.btn)

        return layout

    def listen_to_speech(self, instance):
        try:
            with sr.Microphone() as source:
                self.label.text = "Listening..."
                audio = self.recognizer.listen(source)

                self.label.text = "Processing..."
                text = self.recognizer.recognize_google(audio)
                self.label.text = f"You said: {text}"

        except sr.UnknownValueError:
            self.label.text = "Could not understand audio"
        except sr.RequestError as e:
            self.label.text = f"Could not request results; {e}"


if __name__ == "__main__":
    SpeechToTextApp().run()
