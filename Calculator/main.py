#!/usr/bin/python3
"""A simple calculator."""

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


#Classes
#===============================================================================
class MainScreen(BoxLayout):
    """The main screen for our app."""
    display = ObjectProperty(None)

    def __init__(self, **kwargs):
        """Setup this screen."""
        super(MainScreen, self).__init__(**kwargs)
        self.stack = []

    def store(self):
        """Push the result of the current equation onto the stack."""
        try:
            self.stack.append(eval(self.display.text))
            self.display.text = ""

        except ValueError:
            self.display.text = "Error"

    def load(self):
        """Pop the top of the stack and add it to the end of the current
        equation.
        """
        try:
            self.display.text += str(self.stack.pop())

        except Exception:
            pass

    def solve(self):
        """Solve the current math equation and display the result."""
        try:
            self.display.text = str(eval(self.display.text))

        except ValueError:
            self.display.text = "Error"


class CalculatorApp(App):
    """A basic Kivy app."""
    def build(self):
        return MainScreen()


#Entry Point
#===============================================================================
if __name__ == "__main__":
    CalculatorApp().run()