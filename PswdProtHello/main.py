#!/usr/bin/python3
"""A multi-screen login app."""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager


#Classes
#===============================================================================
class MainScreen(ScreenManager):
    """The main screen for our app."""
    def login(self, name, pswd):
        """Log into this app."""
        return name == "Dylan" and pswd == "cheetah"

    def say_hello(self):
        """Say hello to the current user."""
        self.ids["MsgLbl"].text = "Hello {}!".format(
            self.ids["UsernameInput"].text)
        self.current = "MsgDialog"

    def access_denied(self):
        """Display our access denied message."""
        self.ids["MsgLbl"].text = "***Access Denied***"
        self.current = "MsgDialog"

    def do_login(self):
        """Attempt to login and say hello to the current user."""
        if self.login(self.ids["UsernameInput"].text, 
            self.ids["PasswordInput"].text):
            self.say_hello()

        else:
            self.access_denied()


class PswdProtHelloApp(App):
    """A basic Kivy app."""
    def build(self):
        """Build the GUI for this app."""
        return MainScreen()


#Entry Point
#===============================================================================
PswdProtHelloApp().run()