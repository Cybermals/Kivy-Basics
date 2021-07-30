#!/usr/bin/python3
"""A simple text editor app."""

import os
from os import listdir

import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup

#Apply external storage patch for Android
if kivy.platform == "android":
    from storage import get_external_storage_path


#Classes
#===============================================================================
class ConfirmDialog(ModalView):
    """A confirmation dialog."""
    def __init__(self, **kwargs):
        """Setup this confirmation dialog."""
        super(ConfirmDialog, self).__init__()

        if "msg" in kwargs:
            self.ids["Message"].text = kwargs["msg"]

        if "on_confirm" in kwargs:
            self.ids["Yes"].bind(on_press = kwargs["on_confirm"])
        
        if "on_cancel" in kwargs:
            self.ids["No"].bind(on_press = kwargs["on_cancel"])

    def confirm(self):
        """Confirm the pending operation."""
        self.dismiss()

    def cancel(self):
        """Cancel the pending operation."""
        self.dismiss()


class FileDialog(ModalView):
    """A file dialog."""
    def __init__(self, **kwargs):
        """Setup this file dialog."""
        super(FileDialog, self).__init__()
        self.on_confirm = None
        self.on_cancel = None

        if "mode" in kwargs:
            self.mode = kwargs["mode"]

            if self.mode == "open":
                self.confirm_btn.text = "Open"

            elif self.mode == "save":
                self.confirm_btn.text = "Save"

            elif self.mode == "dir":
                self.confirm_btn.text = "Choose"

        if "path" in kwargs:
            self.files.path = kwargs["path"]

        if "filename" in kwargs:
            self.filename.text = kwargs["filename"]

        if "on_confirm" in kwargs:
            self.on_confirm = kwargs["on_confirm"]

        if "on_cancel" in kwargs:
            self.on_cancel = kwargs["on_cancel"]

        if kivy.platform == "android":
            self.files.root = get_external_storage_path()
            self.files.path = self.files.root

    def confirm(self):
        """Confirm the selected file/dir."""
        if self.mode == "open" and len(self.files.selection) == 1:
            if self.on_confirm is not None:
                self.on_confirm(self)

            self.dismiss()

        elif self.mode == "save" and self.filename.text != "":
            if self.on_confirm is not None:
                self.on_confirm(self)

            self.dismiss()

        else:
            if self.on_confirm is not None:
                self.on_confirm(self)

            self.dismiss()

    def cancel(self):
        """Cancel file/dir selection."""
        self.dismiss()

    def get_path(self):
        """Get the current file/dir."""
        if self.mode == "open" and len(self.files.selection) == 1:
            return self.files.selection[0]

        elif self.mode == "save" and self.filename.text != "":
            return os.path.join(self.files.path, self.filename.text)

        else:
            return self.files.path


class MainScreen(BoxLayout):
    """The main screen of our app."""
    def __init__(self, **kwargs):
        """Setup this app."""
        super(MainScreen, self).__init__(**kwargs)
        self.filename = "./tmp"
        self.popup = None

    def prep_new(self):
        """Prepare to create a new document."""
        msg_dlg = ConfirmDialog(
            msg = "Changes to the current document will be lost. Create new document?", 
            on_confirm = self.new
            )
        msg_dlg.open()

    def new(self, sender):
        """Create a new document."""
        self.document.text = ""

    def prep_open(self):
        """Prepare to open a document."""
        open_dlg = FileDialog(
            mode = "open", 
            path = os.path.dirname(self.filename), 
            filename = os.path.basename(self.filename),
            on_confirm = self.open
            )
        open_dlg.open()

    def open(self, sender):
        """Open a document."""
        self.filename = sender.get_path()

        try:
            with open(self.filename, "r") as f:
                self.document.text = f.read()

        except IOError:
            content = BoxLayout(orientation = "vertical")
            content.add_widget(Label(text = "Failed to open file '{}'".format(
                self.filename)))
            content.add_widget(Button(
                text = "OK", 
                size_hint_y = .125, 
                on_press = self.dismiss_popup
                ))
            self.popup = Popup(title = "Error", content = content)
            self.popup.open()

    def prep_save(self):
        """Prepare to save the current document."""
        save_dlg = FileDialog(
            mode = "save", 
            path = os.path.dirname(self.filename), 
            filename = os.path.basename(self.filename),
            on_confirm = self.save
            )
        save_dlg.open()

    def save(self, sender):
        """Save the current document."""
        self.filename = sender.get_path()

        try:
            with open(self.filename, "w") as f:
                f.write(self.document.text)

        except IOError:
            content = BoxLayout(orientation = "vertical")
            content.add_widget(Label(text = "Failed to save file '{}'".format(
                self.filename)))
            content.add_widget(Button(
                text = "OK", 
                size_hint_y = .125, 
                on_press = self.dismiss_popup
                ))
            self.popup = Popup(title = "Error", content = content)
            self.popup.open()

    def dismiss_popup(self, sender):
        """Dismiss the current popup."""
        self.popup.dismiss()

    def adjust_layout(self, sender, has_focus):
        """Adjust the layout of the app when the virtual keyboard is
        opened/closed.
        """
        if kivy.platform != "android":
            return

        if has_focus:
            self.document.size_hint_y = .6
            self.ids["Filler"].size_hint_y = .4

        else:
            self.document.size_hint_y = .9999
            self.ids["Filler"].size_hint_y = .0001


class NotebookApp(App):
    """A basic Kivy app."""
    def build(self):
        """Build the GUI for this app."""
        return MainScreen()


#Entry Point
#===============================================================================
if __name__ == "__main__":
    NotebookApp().run()
