"""
User interface
"""

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from client import transfer_file


class UserInterface:
    def __init__(self):

        # config the root window
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title('Data Processing')
        self.set_geometry()
        self.browse_file_func()
        self.obj_selection()
        self.serialisation_selection()
        self.encryption_option()
        self.execute_button()
        self.root.mainloop()

    def set_geometry(self):
        """
        Calculates geometry to center the window.

        """

        window_height = 350
        window_width = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    def browse_file_func(self):
        """
        Creates button to upload files.

        """

        # Text for file select label
        file_select_label = ttk.Label( text="Select file for upload:")
        file_select_label.pack(padx=10, pady=5, side= TOP, anchor="w")

        # create a combobox
        selected_file = tk.StringVar()
        file_path = ttk.Combobox(self.root, textvariable=selected_file)

        def select_file():
            """
            Selects file path.

            """

            file_path = askopenfile(mode='r', filetypes=[('text files', '.txt')])
            if file_path is not None:
                pass
            self.file_path = file_path.name

        file_path_button = tk.Button(
            self.root,
            text='Select File',
            command=lambda: select_file(),

        )

        file_path_button.config(width=10)
        file_path_button.pack( padx=10, pady=5, ipadx=2,ipady=3,side= TOP, anchor="w")

        # prevent typing a value
        file_path['state'] = 'readonly'

    def serialisation_selection(self):
        """
        Creates drop down menu to select serialisation method.
        Methods: json, binary, xml.

        """

        # label2 ("Please select the serialisation method"
        serialisation_label = ttk.Label(text="Select serialisation method:")
        serialisation_label.pack( padx=10, pady=5,side= TOP, anchor="w")

        # create a combobox
        selected_method = tk.StringVar()
        serialisation_method = ttk.Combobox(self.root, textvariable=selected_method)

        serialisation_method['values'] = ["XML", "Binary", "Json"]

        # prevent typing a value
        serialisation_method['state'] = 'readonly'

        # place the widget
        serialisation_method.config(width=10)
        serialisation_method.pack( padx=10, pady=5,side= TOP, anchor="w")

    def obj_selection (self):
        """
        Creates drop down menu to select from sample objects.
        Object types: dictionaries, lists

        """

        # label2 ("Please select the serialisation method"
        obj_selection_label = ttk.Label(text="Select object for upload:")
        obj_selection_label.pack( padx=10, pady=5, side= TOP, anchor="w")

        # create a combobox
        selected_object = tk.StringVar()
        selection_obj = ttk.Combobox(self.root, textvariable=selected_object)

        selection_obj['values'] = ["Dictionary 1", "Dictionary 2"]

        # prevent typing a value
        selection_obj['state'] = 'readonly'

        # place the widget
        selection_obj.config(width=10)
        selection_obj.pack( padx=10, pady=5,side= TOP, anchor="w")

    def encryption_option(self):
        """
        Creates tick box to select encryption method.
        Encryption options - Yes, No.

        """

        encryption_label = ttk.Label(text="Encrypt file:")
        encryption_label.pack( padx=10, pady=5, side= TOP, anchor="w")

        var_yes = tk.IntVar()
        Checkbutton(self.root, text="Yes", variable=var_yes).pack( padx=10, pady=5,side= TOP, anchor="w")

        var_no = tk.IntVar()
        Checkbutton(self.root, text="No", variable=var_no).pack( padx=10, pady=5,side= TOP, anchor="w")

    def execute_button(self):
        """
        Executes operation.

        """

        def file_transfer_callback():
            showinfo(
                title='Information',
                message='File transfer initiated'
            )
            transfer_file("0.0.0.0", 5006, self.file_path)

        execute_button = tk.Button(self.root, text="Upload", command=file_transfer_callback)
        execute_button.config(width=10)
        execute_button.pack()



UserInterface()



