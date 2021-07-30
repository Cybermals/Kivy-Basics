#!/usr/bin/python3
"""An app that says hi to you."""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


#Classes
#===============================================================================
class MainScreen(BoxLayout):
    """The main screen of this app."""
    def say_hello(self):
        """Say hello to the user."""
        self.ids["MsgLbl"].text = "Hello {}!".format(self.ids["NameInput"].text)


class HelloApp(App):
    """A basic Kivy app."""
    def build(self):
        """Build the GUI."""
        return MainScreen()


#Entry Point
#===============================================================================
HelloApp().run()