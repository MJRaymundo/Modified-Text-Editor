# Mark john M. Raymundo CoE 2-2 Data Structure and Algorithms
# Text Editor Project by github user: iampiyushjain, modified to contain additional features
# Source Link: https://github.com/iampiyushjain/Text-Editor
# Modified Parts : Added Search and Sorting Options in Edit Menu.

from Window import *

TextEditor = Window()

TextEditor.TextBox.pack(expand=1, fill="both")
TextEditor.window.protocol("WM_DELETE_WINDOW", TextEditor.on_closing)
TextEditor.window.bind("<Key>", TextEditor.key_pressed)
TextEditor.window.mainloop()
