# Mark john M. Raymundo CoE 2-2 Data Structure and Algorithms
# Modified Text Editor Project by github user: iampiyushjain
# Source Link: https://github.com/iampiyushjain/Text-Editor
# Modified Parts : Added Search and Sorting Options in Edit Menu.

from tkinter import *
from tkinter import messagebox as message
from tkinter import filedialog as fd
from Stack import *
import re


#  Class Window is used for managing all the operations in TextEditor
class Window:
    def __init__(self):
        # Variables declarations at initial level
        self.isFileOpen = True
        self.File = ""
        self.isFileChange = False
        self.elecnt = 0
        self.mode = "normal"
        self.fileTypes = [('All Files', '*.*'),
                          ('Python Files', '*.py'),
                          ('Text Document', '*.txt')]

        # Initialisation Of window
        self.window = Tk()
        self.window.geometry("1200x700+200+150")
        self.window.wm_title("Untitled")

        # Initialisation of Text Widget
        self.TextBox = Text(self.window, highlightthickness=0, font=("Helvetica", 14))

        # Initialisation of MenuBar
        self.menuBar = Menu(self.window, bg="#eeeeee", font=("Helvetica", 13), borderwidth=0)
        self.window.config(menu=self.menuBar)
        # File Menu
        self.fileMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2, font="Helvetica")
        self.fileMenu.add_command(label="    New       Ctrl+N", command=self.new_file, )
        self.fileMenu.add_command(label="    Open...      Ctrl+O", command=self.open_file)
        self.fileMenu.add_command(label="    Save         Ctrl+S", command=self.retrieve_input)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="    Exit          Ctrl+D", command=self._quit)
        self.menuBar.add_cascade(label="   File   ", menu=self.fileMenu)
        # Edit Menu
        self.editMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2,
                             font="Helvetica", )
        self.editMenu.add_command(label="    Undo    Ctrl+Z", command=self.undo)
        self.editMenu.add_command(label="    Redo    Ctrl+Shift+Z", command=self.redo)
        self.editMenu.add_separator()
        self.editMenu.add_command(label="    Cut    Ctrl+X", command=self.cut)
        self.editMenu.add_command(label="    Copy    Ctrl+C", command=self.copy)
        self.editMenu.add_command(label="    Paste   Ctrl+V", command=self.paste)
        # Added/Modified a "Search" Function
        self.editMenu.add_command(label="    Search   ", command=self.search)
        self.editMenu.add_command(label="    Sorting by line (Ascending)  ", command=self.sortingascending)
        self.editMenu.add_command(label="    Sorting by line (Descending)  ", command=self.sortingdescending)
        self.menuBar.add_cascade(label="   Edit   ", menu=self.editMenu)
        # View Menu
        self.viewMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2,
                             font="Helvetica", )
        self.viewMenu.add_command(label="   Change Mode   ", command=self.change_color)
        self.menuBar.add_cascade(label="   View   ", menu=self.viewMenu)
        # Help Menu
        self.helpMenu = Menu(self.menuBar, tearoff=0, activebackground="#d5d5e2", bg="#eeeeee", bd=2,
                             font="Helvetica", )
        self.helpMenu.add_command(label="    About   ", command=self.about)
        self.menuBar.add_cascade(label="   Help   ", menu=self.helpMenu)

        # Initialisation Of Stack Objects By Original state i.e if the file contains data, it is the Original state of
        # that file
        self.UStack = Stack(self.TextBox.get("1.0", "end-1c"))
        self.RStack = Stack(self.TextBox.get("1.0", "end-1c"))

    #     Member Functions
    # 1. New File method which creates a new file
    def new_file(self):
        self.TextBox.config(state=NORMAL)
        if self.isFileOpen:
            if len(self.File) > 0:
                if self.isFileChange:
                    self.save_file(self.File)
                self.window.wm_title("Untitled")
                self.TextBox.delete('1.0', END)
                self.File = ''
            else:
                if self.isFileChange:
                    result = message.askquestion('Window Title', 'Do You Want to Save Changes')
                    self.save_new_file(result)
                self.window.wm_title("Untitled")
                self.TextBox.delete('1.0', END)
        else:
            self.isFileOpen = True
            self.window.wm_title("Untitled")

        self.isFileChange = False

        if self.UStack.size() > 0:
            self.UStack.clear_stack()
            self.UStack.add(self.TextBox.get("1.0", "end-1c"))

    # 2. Open a file which opens a file in editing mode
    def open_file(self):
        self.TextBox.config(state=NORMAL)
        if self.isFileOpen and self.isFileChange:
            self.save_file(self.File)
        filename = fd.askopenfilename(filetypes=self.fileTypes, defaultextension=".txt")
        if len(filename) != 0:
            self.isFileChange = False
            outfile = open(filename, "r")
            text = outfile.read()
            self.TextBox.delete('1.0', END)
            self.TextBox.insert(END, text)
            self.window.wm_title(filename)
            self.isFileOpen = True
            self.File = filename

        if self.UStack.size() > 0:
            self.UStack.clear_stack()
            self.UStack.add(self.TextBox.get("1.0", "end-1c"))

    # 3. Save file
    def save_file(self, file):
        result = message.askquestion('Window Title', 'Do You Want to Save Changes')
        if result == "yes":
            if len(file) == 0:
                saveFile = fd.asksaveasfile(filetypes=self.fileTypes, defaultextension=".txt")
                print(saveFile.name)
                self.write_file(saveFile.name)
                self.TextBox.delete('1.0', END)
            else:
                self.write_file(file)

    # 4. Save new file -> this function is for saving the new file
    def save_new_file(self, result):
        self.isFileChange = False
        if result == "yes":
            saveFile = fd.asksaveasfile(filetypes=self.fileTypes, defaultextension=".txt")
            self.write_file(saveFile.name)
            self.File = saveFile.name
        else:
            self.TextBox.delete('1.0', END)

    # 5. Writing in file
    def write_file(self, file):
        inputValue = self.TextBox.get("1.0", "end-1c")
        outfile = open(file, "w")
        outfile.write(inputValue)

    # 6. Getting the data from file and showing in the text widget box
    def retrieve_input(self):
        if self.isFileOpen and len(self.File) != 0:
            self.write_file(self.File)
            self.isFileChange = False
        else:
            self.save_new_file("yes")
            self.window.wm_title(self.File)
            self.isFileOpen = True

    # 7. This function invokes whenever a key is pressed whether it is a special-key or a normal key
    def key_pressed(self, event):
        if event.char == "\x1a" and event.keysym == "Z":
            self.redo()
        elif event.char == "\x1a" and event.keysym == "z":
            self.undo()
        elif event.char == "\x13":
            self.retrieve_input()
        elif event.char == "\x0f":
            self.open_file()
        elif event.char == "\x0e":
            self.new_file()
        elif event.char == "\x04":
            self._quit()
        elif event.char == " " or event.char == ".":
            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")
            self.UStack.add(inputValue)
        elif event.keysym == 'Return':
            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")
            self.UStack.add(inputValue)
        elif event.keysym == 'BackSpace':
            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")
            self.UStack.add(inputValue)
        elif (event.keysym == 'Up' or event.keysym == 'Down') or (event.keysym == 'Left' or event.keysym == 'Right'):
            self.isFileChange = True
            self.elecnt = 0
            inputValue = self.TextBox.get("1.0", "end-1c")
            self.UStack.add(inputValue)
        else:
            self.isFileChange = True
            inputValue = self.TextBox.get("1.0", "end-1c")
            if self.elecnt >= 1:
                self.UStack.remove()
            self.UStack.add(inputValue)
            self.elecnt += 1

        if self.TextBox.get("1.0", "end-1c") == self.UStack.ele(0):
            self.isFileChange = False

    # 8. Undo the data by calling Stack class functions
    def undo(self):
        self.isFileChange = True
        if self.UStack.size() == 1:
            self.UStack.remove()
            self.UStack.add(self.TextBox.get("1.0", "end-1c"))
        else:
            self.RStack.add(self.UStack.remove())
            text = self.UStack.peek()
            self.TextBox.delete('1.0', END)
            self.TextBox.insert(END, text)

    # 9. Redo/Rewrite the task/data by calling Stack class functions
    def redo(self):
        if self.RStack.size() > 1:
            text = self.RStack.peek()
            self.TextBox.delete('1.0', END)
            self.TextBox.insert(END, text)
            self.UStack.add(text)
            self.RStack.remove()

    # 10. Close the window (called when the close button at the right-top is clicked)
    def on_closing(self):
        if self.isFileOpen and self.isFileChange:
            self.save_file(self.File)
        self._quit()

    # 11. Quit or Exit Function to exit from Text-Editor
    def _quit(self):
        self.window.quit()
        self.window.destroy()

    # 12. Night mode view by changing the color of Text widget
    def change_color(self):

        if self.mode == "normal":
            self.mode = "dark"
            self.TextBox.configure(background="#2f2b2b", foreground="#BDBDBD", font=("Helvetica", 14),
                                   insertbackground="white")
        else:
            self.mode = "normal"
            self.TextBox.configure(background="white", foreground="black", font=("Helvetica", 14),
                                   insertbackground="black")

    # 13. About
    def about(self):
        outfile = open("About.txt", "r")
        text = outfile.read()
        self.TextBox.insert(END, text)
        self.TextBox.config(state=DISABLED)

    # 14. Copy
    def copy(self):
        self.TextBox.clipboard_clear()
        text = self.TextBox.get("sel.first", "sel.last")
        self.TextBox.clipboard_append(text)

    # 15. Cut
    def cut(self):
        self.copy()
        self.TextBox.delete("sel.first", "sel.last")
        self.UStack.add(self.TextBox.get("1.0", "end-1c"))

    # 16. Paste
    def paste(self):
        text = self.TextBox.selection_get(selection='CLIPBOARD')
        self.TextBox.insert('insert', text)
        self.UStack.add(self.TextBox.get("1.0", "end-1c"))

    # Modified Function #1
    # 17. Search 
    def search(self):
        # Window for Search Box
        search_window = Toplevel(self.window)
        search_window.geometry("300x100+300+250")
        search_window.wm_title("Search")

        # Entry Box
        search_label = Label(search_window, text="Enter search term:")
        search_label.grid(row=0, column=0, padx=5, pady=10)
        search_entry = Entry(search_window, width=30)
        search_entry.grid(row=0, column=1, padx=5, pady=10)

        # Define Terms
        text = self.TextBox

        # Finding the word function
        def find_text():
            text.tag_remove('found', 1.0, END)
            word = search_entry.get()
            if word:
                idx = '1.0'
                while 1:
                    idx = text.search(word, idx, nocase=1, stopindex=END)
                    if not idx: break
                    lastidx = '%s+%dc' % (idx, len(word))
                    text.tag_add('found', idx, lastidx)
                    idx = lastidx
                text.tag_config('found', foreground= 'red')
            search_entry.focus_set()

            def on_closing():
                if self.mode == "normal":
                    text.tag_config('found', foreground='black')
                else:
                    text.tag_config('found', foreground='BDBDBD')
                search_window.destroy()

            search_window.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Cancel Button
        def cancel():
            if self.mode == "normal":
                text.tag_config('found', foreground='black')
            else:
                text.tag_config('found', foreground='BDBDBD')
            search_window.destroy()

        # Buttons
        search_button = Button(search_window, text="Search", command=find_text)
        search_button.grid(row=1, column=0, padx=5, pady=10)
        cancel_button = Button(search_window, text="Cancel", command=cancel)
        cancel_button.grid(row=1, column=1, padx=5, pady=10)

    # Modified Function #2
    # 18. Sorting text by line in ascending Order
    # A. Sort by line (Ascending) Method
    def sortingascending(self):
        # Get the text from the Text widget
        txt = self.TextBox.get("1.0", "end-1c")
        # Split the text into lines
        lines = txt.split("\n")
        # Sort the lines in ascending order
        sorted_lines = self.fileMenumerge_sort(lines)
        # Join the sorted lines back into text
        sorted_text = "\n".join(sorted_lines)
        # Update the Text widget with the sorted text
        self.TextBox.delete("1.0", "end")
        self.TextBox.insert(END, sorted_text)

    def sortingdescending(self):
        # Get the text from the Text widget
        txt = self.TextBox.get("1.0", "end-1c")
        # Split the text into lines
        lines = txt.split("\n")
        # Sort the lines in descending order
        sorted_lines = self.fileMenumerge_sort(lines)[::-1]
        # Join the sorted lines back into text
        sorted_text = "\n".join(sorted_lines)
        # Update the Text widget with the sorted text
        self.TextBox.delete("1.0", "end")
        self.TextBox.insert(END, sorted_text)

    def fileMenumerge_sort(self, lines):
        # Define the merge function
        def merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] < right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result += left[i:]
            result += right[j:]
            return result

        # Define the merge_sort function
        def merge_sort(lst):
            if len(lst) <= 1:
                return lst
            mid = len(lst) // 2
            left = merge_sort(lst[:mid])
            right = merge_sort(lst[mid:])
            return merge(left, right)

        # Sort the lines in ascending order
        sorted_lines = merge_sort(lines)

        return sorted_lines