#!/usr/bin/python3
"""A basic hello world app."""

from kivy.app import App
from kivy.uix.label import Label


#Classes
#===============================================================================
class HelloApp(App):
    """A basic Kivy app."""
    def build(self):
        """Build the UI."""
        return Label(text = "Hello World!")


#Entry Point
#===============================================================================
HelloApp().run()