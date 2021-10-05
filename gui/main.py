from kivy.app import App
from kivy.uix.widget import Widget
# from kivy.uix.button import Label
# from kivy.uix.textinput import TextInput
# from kivy.properties import NumericProperty, Clock
# from kivy.graphics.vertex_instructions import Line
# from kivy.graphics.context_instructions import Color
# from kivy.core.window import Window
# from kivy import platform
# from kivy.config import Config


class MainWidget(Widget):
    pass


class RootPageApp(App):
    # def build(self):
    #     return MainWidget()
    pass

    # def on_enter(instance, value):
    #     print('User pressed enter in', instance)

    # def on_text(instance, value):
    #     print('The widget', instance, 'have:', value)

    # def build(self):
    #     label = Label(text="Hello Kivy...")

    #     textinput = TextInput(text='Hello world')

    #     textinput = TextInput()
    #     textinput.bind(text=on_text)

    #     textinput = TextInput(text='Hello world', multiline=False)
    #     textinput.bind(on_text_validate=on_enter)

    #     self.add_widget(Label)
    #     self.add_widget(textinput)

    # class RootPageApp(App):
    #     def build(self):
    #         return Label()


if __name__ == "__main__":
    RootPageApp().run()

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
