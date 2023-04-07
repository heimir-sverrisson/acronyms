#!/usr/bin/env python3
#
import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMessageBox
)
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QEvent
from main_window_ui import Ui_MainWindow

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, filename, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.acronymText.installEventFilter(self)
        self.acronyms = []
        self.read_acronyms(filename)

    def connectSignalsSlots(self):
        self.action_Exit.triggered.connect(self.close)
        self.action_About.triggered.connect(self.about)

    def eventFilter(self, obj, event):
        if obj is self.acronymText and event.type() == QEvent.KeyPress:
            current_string = self.acronymText.toPlainText()
            new_string = current_string
            key = event.key()
            if key in (Qt.Key_Enter, Qt.Key_Return):
                return True     # Disable new line
            if key == Qt.Key_Backspace:
                new_string = current_string[0:-1] # Remove last character
            elif len(event.text()) > 0:
                new_string += event.text()  # Regular text
            else:
                return True     # Ignore all other keys
            # self.acronymList.appendPlainText(f' {new_string} + {event.key()}')
            self.search(new_string)
        return super(Window, self).eventFilter(obj, event)

    def about(self):
        QMessageBox.about(
            self,
            "About Acronym Finder",
            "<p>Find the meaning of an acronym</p>"
            "<p>Heimir Þór Sverrisson, 2023</p>"
            "<p>W1ANT / TF3ANT</p>"
        )


    def read_acronyms(self, filename):
        with open(filename) as file:
            self.acronyms = [line.strip() for line in file]

    def search(self, search):
        self.acronymList.clear()
        if len(search) == 0:
            return
        expr = f'^{search}'
        for a in self.acronyms:
            if re.search(expr, a, re.IGNORECASE):
                self.acronymList.appendPlainText(f'{a} ')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window("acronyms.txt")
    win.show()
    win.acronymText.setFocus()
    sys.exit(app.exec())