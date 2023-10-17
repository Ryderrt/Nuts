from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
from file import File


# --------------------------------------------------------------
# ---------------------- CUSTOM WIDGETS ------------------------
# --------------------------------------------------------------

class AutoScrollbar(Scrollbar):

    def set(self, low, high):
        # The set method for the Scrollbar class takes lo and hi
        # values between 0 and 1. These represent the postion of
        # the scrollbar along the tube (0 is the top of the screen,
        # 1 is the bottom). So if low <= 0 and high >= 0, the scroll
        # bar doesn't need to be displayed, since it can't be moved.
        if float(low) <= 0.0 and float(high) >= 1.0:               
            self.grid_remove(self)
        else:
            self.grid()
        Scrollbar.set(self, low, high)

# --------------------------------------------------------------
# ------------------------ MENU ITEMS --------------------------
# --------------------------------------------------------------

# FILE MENU ITEMS

# These 2 are just helper functions, kind of repetitive but it works
def make_new_file(text: Text, root: Tk):
    text.delete("1.0", END)
    root.title("New file - Nuts")

def del_make_new_file(text: Text, root: Tk, check_win: Toplevel):
    check_win.destroy()
    make_new_file(text=text, root=root)
    text.edit_modified(False)

def new_file(text: Text, root: Tk):
    if not text.edit_modified(): # edit_modified returns true if the text has been edited
        make_new_file(text=text, root=root)
        text.edit_modified(False)
    else: 
        # Create an "are you sure?" window
        check_win = Toplevel(); check_win.grid()
        check_win.title("Are you sure?")
        
        lbl = Label(check_win, text="Project is unsaved, are you sure you want to delete it?")
        lbl.grid(column=0, row=0, columnspan=2, padx=20, pady=20)
        cancel_btn = Button(check_win, text="Cancel", command=check_win.destroy)
        cancel_btn.grid(column=0, row=1, sticky=(N,E,S,W))
        delete_btn = Button(check_win, text="Delete", background="red", command=lambda: del_make_new_file(text=text, root=root, check_win=check_win))
        delete_btn.grid(column=1, row=1, sticky=(N,E,S,W))

def open_file(text: Text, root: Tk):
    # Clear the text area
   # new_file(text=text, root=root)
    # Open system file manager
    filepath = filedialog.askopenfilename(initialdir="/home/alexander/",
                                          title="Open file",
                                          filetypes=(("Text Files", "*.txt"), ("Python Files", "*.py")))
    # Check we haven't just pressed cancel on the dialog
    if filepath:
        CURRENT_FILE = filepath
        NAMED = True
        with open(filepath, 'r') as file:
            contents = file.read()
        text.insert('1.0', contents)
        # Need to add if else here based on what platform you're on
        root.title(filepath.split("/")[-1].split(".")[0] + "- Nuts") # set title to filename minus the .txt
        text.edit_modified(False) # the file has not been edited

def save_file(text: Text, root: Tk):
    if not NAMED:
        filepath = filedialog.asksaveasfilename(defaultextension=".txt")
        if (filepath != ()):
            CURRENT_FILE = filepath
            with open(filepath, 'w') as file:
                file.write(text.get('1.0', END))
            NAMED = True
            root.title(filepath.split("/")[-1].split(".")[0] + "- Nuts")
    else:
        with open(CURRENT_FILE, 'w') as file:
            file.write(text.get('1.0', END))

def save_as(text: Text, root: Tk):
    filepath = filedialog.asksaveasfilename(defaultextension=".txt")
    if (filepath != ()):
        with open(filepath, 'w') as file:
            file.write(text.get('1.0', END))
        root.title(filepath.split("/")[-1].split(".")[0] + "- Nuts")
        text.edit_modified(False) # Since the file has just been saved, it has not been edited since last save

# EDIT MENU ITEMS

def increase_text_size(text: Text):
    text.config(font=("Arial", 20))

def select_all(text: Text):
    text.tag_add(SEL, 1.0, END)
    return 'break'


    
# APPEARANCE MENU ITEMS

def toggle_dark_theme(text: Text):
    text['background'] = "black"
    text['foreground'] = "white"
    text['insertbackground'] = "white"

def toggle_light_theme(text: Text):
    text['background'] = "white"
    text['foreground'] = "black"
    text['insertbackground'] = "black"

# --------------------------------------------------------------
# --------------------------- MAIN -----------------------------
# --------------------------------------------------------------

def main():
    root = Tk()
    root.geometry("800x650")
    root.title("New file - Nuts")
    root.option_add("*tearOff", FALSE)

    f = ttk.Frame(root); f.grid(column=0, row=0, sticky=(N,W,E,S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # -------- Text area --------

    text = Text(root, wrap="word"); text.grid(column=0, row=0, sticky=(N,W,E,S))
    # auto_scroll = AutoScrollbar(root, orient="vertical", command=text.yview)
    # text['yscrollcommand'] = auto_scroll.set
    # auto_scroll.grid(column=1, row=0, sticky="ns")

    # Turn undo-ability on
    text['undo'] = True
    
    text.focus()

    # -- Keybinds --
    # The bind fn. will always send an Event parameter to the fn. explaining the seemingly redundant "event" parameter


    # -------- Menu --------

    menubar = Menu(root)
    root['menu'] = menubar

    menu_file = Menu(menubar)
    menu_edit = Menu(menubar)
    menu_appearance = Menu(menubar)
    menubar.add_cascade(menu=menu_file, label='File')
    menubar.add_separator()
    menubar.add_cascade(menu=menu_edit, label='Edit')
    menubar.add_separator()

    menubar.add_cascade(menu=menu_appearance, label='Appearance')

    # File
    menu_file.add_command(label='New', command=lambda: new_file(text=text, root=root))
    menu_file.add_command(label='Open', command=lambda: open_file(text=text, root=root))
    menu_file.add_command(label='Save', command=lambda: save_file(text=text, root=root))
    menu_file.add_command(label='Save As', command=lambda: save_as(text=text, root=root))
    # Edit
    menu_edit.add_command(label='Select all', command=lambda: select_all(text=text))
    menu_edit.add_separator()
    menu_edit.add_command(label='Undo', command=text.edit_undo)
    menu_edit.add_command(label='Redo', command=text.edit_redo)
    # Appearance
    menu_appearance.add_radiobutton(label='Light Theme', command=lambda: toggle_light_theme(text))
    menu_appearance.add_radiobutton(label='Dark Theme', command=lambda: toggle_dark_theme(text))

    # -- Menu Binds --
    # File
    text.bind("<Control-o>", lambda event: open_file(text=text, root=root))
    text.bind("<Control-n>", lambda event: new_file(text=text, root=root))
    text.bind("<Control-S>", lambda event: save_as(text=text, root=root))
    # Edit
    text.bind("<Control-a>", lambda event: select_all(text=text))
    text.bind("<Control-z>", lambda event: text.edit_undo)
    # Ideally, id like ctrl-y to be redo, but for some reason its bound to paste and i cant seem to change it
    text.bind("<Control-Z>", lambda event: text.edit_redo)
    # Appearance
    text.bind("<Control-plus>", lambda event: increase_text_size(text=text))

    root.mainloop()


if __name__ == '__main__':
    main()