# from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.uix.button import Label
# from kivy.uix.textinput import TextInput
# from kivy.properties import NumericProperty, Clock
# from kivy.graphics.vertex_instructions import Line
# from kivy.graphics.context_instructions import Color
# from kivy.core.window import Window
# from kivy import platform
# from kivy.config import Config


# class MainWidget(Widget):
#     pass


# class RootPageApp(App):
#     def build(self):
#         return MainWidget()

#     def on_enter(instance, value):
#         print('User pressed enter in', instance)

#     def on_text(instance, value):
#         print('The widget', instance, 'have:', value)

#     def build(self):
#         label = Label(text="Hello Kivy...")

#         textinput = TextInput(text='Hello world')

#         textinput = TextInput()
#         textinput.bind(text=on_text)

#         textinput = TextInput(text='Hello world', multiline=False)
#         textinput.bind(on_text_validate=on_enter)

#         self.add_widget(Label)
#         self.add_widget(textinput)

#     class RootPageApp(App):
#         def build(self):
#             return Label()


# if __name__ == "__main__":
#     RootPageApp().run()

# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout


# class Threebythreeone(BoxLayout):
#     pass


# class Noughtsandcrosses(BoxLayout):
#     pass


# class nandxApp(App):
#     def build(self):
#         return Noughtsandcrosses()


# if __name__ == "__main__":
#     nandxApp().run()

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        self.reset()
        sm.current = "login"
        # if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
        #     if self.password != "":
        #         db.add_user(self.email.text, self.password.text, self.namee.text)

        #         self.reset()

        #         sm.current = "login"
        #     else:
        #         invalidForm()
        # else:
        #     invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        self.reset()
        sm.current = "main"
        # if db.validate(self.email.text, self.password.text):
        #     MainWindow.current = self.email.text
        #     self.reset()
        #     sm.current = "main"
        # else:
        #     invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        pass
        # password, name, created = db.get_user(self.current)
        # self.n.text = "Account Name: " + name
        # self.email.text = "Email: " + self.current
        # self.created.text = "Created On: " + created


class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(
                    text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
# db = DataBase("users.txt")

screens = [LoginWindow(name="login"), CreateAccountWindow(
    name="create"), MainWindow(name="main")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()
