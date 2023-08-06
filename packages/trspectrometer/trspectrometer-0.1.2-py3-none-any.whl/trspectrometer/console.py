#!/usr/bin/env python3

# Copyright 2020 Patrick C. Tapping
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import os, sys, io, readline, rlcompleter, atexit
from PySide2 import QtCore, QtWidgets              #pylint: disable=import-error
from PySide2.QtUiTools import loadUiType           #pylint: disable=no-name-in-module
from PySide2.QtCore import QEvent                  #pylint: disable=no-name-in-module

"""A simple but functional GUI Python console implemented in PySide2."""

# TODO: Handle multi-line expressions. Could be done by attempting to
# code.compile the command or just look for an unexpected EOF SyntaxError and
# begin to compound input lines.
# TODO: Handle exit better. If embedded in another application, then we don't
# want to exec exit(). Maybe implement a "exit" signal or similar.

class Console(QtWidgets.QMainWindow, loadUiType(__file__.split(".py")[0] + ".ui")[0]):
    """
    The Console class implements a GUI Python console.

    The Console may be instantiated with a function that should return a
    dictionary of the namespace in which the console will operate. The function
    will be evaluated prior to executing each command. The default behaviour if
    no namespace_func is provided is to call globals().

    The command history will be stored in a file named .console_history by
    default. An alternative path may be provided in the constructor.

    :param namespace_func: A function used to obtain a namespace dictionary prior
        to executing each command.
    :param history_filename: Path and filename of file to store the command history.
    """

    def __init__(self, namespace_func=globals, history_filename=".console_history"):
        super().__init__()
        self.setupUi(self)

        self.namespace_func=namespace_func

        # Set up command history
        self.history_filename = history_filename
        readline.set_history_length(1000)
        try:
            readline.read_history_file(self.history_filename)
        except FileNotFoundError:
            pass
        self.history_i = readline.get_current_history_length() + 1
        atexit.register(readline.write_history_file, self.history_filename)

        # Set up up/down history and tab completion
        self.inputbox.installEventFilter(self)

        # Handle enter key press
        self.inputbox.returnPressed.connect(self.do_command)

    def do_command(self):
        """Trigger the execution of the command currently in the input text box."""
        if self.inputbox.text() != "":
            try:
                self.outputbox.appendPlainText(">>> {}".format(self.inputbox.text()))
                # Note that on Linux, asking for a non-existent history index returns nothing,
                # but on Windows, an array out-of-bounds exception will be raised.
                if readline.get_current_history_length() == 0 or (readline.get_current_history_length() > 0 and self.inputbox.text() != readline.get_history_item(readline.get_current_history_length())):
                    readline.add_history(self.inputbox.text())
                self.history_i = readline.get_current_history_length() + 1
                ns = self.namespace_func() if callable(self.namespace_func) else None
                old_stdout = sys.stdout
                sys.stdout = io.StringIO(newline=None)
                ans = ""
                output = ""
                try:
                    ans = str(eval(self.inputbox.text(),  ns))
                except SyntaxError:
                    exec(self.inputbox.text(), ns)
                output = sys.stdout.getvalue().rstrip('\r\n')
                if len(output) > 0: self.outputbox.appendPlainText(output)
                if len(ans) > 0: self.outputbox.appendPlainText(ans)
            except Exception as ex:
                self.outputbox.appendPlainText("{}: {}".format(type(ex).__name__, ex))
                pass
            except SystemExit as ex:
                self.outputbox.appendPlainText("To exit, close all windows.")
            sys.stdout = old_stdout
            self.inputbox.setText("")

    def eventFilter(self, target, event):
        """Filter events on the inputbox to catch autocomplete/history keys."""
        if event.type() == QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Tab:
                completer = rlcompleter.Completer(self.namespace_func() if callable(self.namespace_func) else None)
                completions = []
                split_index = max([self.inputbox.text().rfind(sep) for sep in '()[] ']) + 1
                while True:
                    try:
                        completion = completer.complete(self.inputbox.text()[split_index:], len(completions))
                    except AttributeError:
                        # Work around for "redisplay" missing bug in readline on Windows
                        completion = None
                    if completion:
                        completions.append(completion)
                    else:
                        break
                if len(completions) == 1:
                    self.inputbox.setText(self.inputbox.text()[:split_index] + completions[0])
                elif len(completions) > 1:
                    self.outputbox.appendPlainText("Possible completions:")
                    [ self.outputbox.appendPlainText(' ' + c) for c in completions ]
                return True
            elif event.key() == QtCore.Qt.Key_Down and readline.get_current_history_length():
                self.history_i = min(self.history_i + 1, readline.get_current_history_length() + 1)
                self.inputbox.setText(readline.get_history_item(self.history_i) if self.history_i <= readline.get_current_history_length() else "")
            elif event.key() == QtCore.Qt.Key_Up and readline.get_current_history_length():
                self.history_i = max(self.history_i - 1, 1)
                self.inputbox.setText(readline.get_history_item(self.history_i))
        return False

def main():
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = Console()
    mainwindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
