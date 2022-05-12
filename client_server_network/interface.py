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

import tkinter as tk

# root = tk.Tk()

# frame1 = tk.Frame(root, highlightbackground="white", highlightthickness=1)
# frame1.pack(side=tk.TOP, padx=10, pady=1,fill= BOTH, expand= True)
# frame2 = tk.Frame(root, highlightbackground="white", highlightthickness=1)
# frame2.pack(side=tk.BOTTOM, padx=10, pady=1,fill= BOTH, expand= True)
#
# t1 = tk.Label(frame1, text="Hello:")
# b1 = tk.Button(frame1, text='b1')
# t2 = tk.Label(frame1, text="Bye:")
# b2 = tk.Button(frame1, text='b2')
# t1.pack(side=tk.LEFT)      # pack starts packing widgets on the left
# b1.pack(side=tk.LEFT)      # pack starts packing widgets on the left
# t2.pack(side=tk.LEFT)
# b2.pack(side=tk.LEFT)
#
# b3 = tk.Button(frame2, text='b3')
# b3.pack(side=tk.LEFT)
# root.mainloop()

class UserInterface:
    def __init__(self):

        # config the root window
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title('Data Processing')
        self.set_geometry()
        self.outer_frame = tk.Frame(self.root, highlightbackground="white", highlightthickness=1)
        self.outer_frame.pack(padx=0, pady=5,expand=False)
        self.frame1 = tk.Frame(self.outer_frame, highlightbackground="white", highlightthickness=1)
        self.frame1.pack(side=tk.TOP, fill=BOTH, expand=False)
        self.sub_frame = tk.Frame(self.frame1)
        self.sub_frame.pack(anchor=CENTER, padx=10, pady=5)
        self.frame2 = tk.Frame(self.outer_frame, highlightbackground="white", highlightthickness=1)
        self.frame2.pack(side=tk.TOP, fill=BOTH, expand=False)
        self.frame3 = tk.Frame(self.outer_frame, highlightbackground="white", highlightthickness=1)
        self.frame3.pack(side=tk.TOP, fill=BOTH, expand=False)
        self.frame4 = tk.Frame(self.outer_frame, highlightbackground="white", highlightthickness=1)
        self.frame4.pack(side=tk.TOP, fill=BOTH, expand=False)
        self.frame5 = tk.Frame(self.outer_frame, highlightbackground="white", highlightthickness=1)
        self.frame5.pack(side=tk.TOP, fill=BOTH, expand=False)
        self.browse_file_func()
        self.obj_selection()
        self.serialisation_selection()
        self.encryption_option()
        self.execute_button()
        self.text_box_func()
        self.root.mainloop()

    def set_geometry(self):
        """
        Calculates geometry to center the window.

        """

        window_height = 550
        window_width = 650
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    def browse_file_func(self):
        """
        Creates button to upload files.
        """
        file_select = ttk.Label(self.sub_frame, text="Select file or object for transfer:")
        file_select.pack(padx=10, pady=5)


        # Text for file select label
        file_select_label = ttk.Label(self.sub_frame, text="Select file:")
        file_select_label.pack(padx=10, pady=5,side=LEFT)

        # create a combobox
        selected_file = tk.StringVar()
        file_path = ttk.Combobox(self.sub_frame, textvariable=selected_file)

        def select_file():
            """
            Selects file path
            """

            file_path = askopenfile(mode='r', filetypes=[('text files', '.txt')])
            if file_path is not None:
                pass
            self.file_path = file_path.name
            self.T.insert("1.0",f"File Path selected: {self.file_path}")

        file_path_button = tk.Button(
            self.sub_frame,
            text='Browse',
            command=lambda: select_file(),
        )

        file_path_button.config(width=10)
        file_path_button.pack(padx=10, pady=5, side=LEFT)

        # prevent typing a value
        file_path['state'] = 'readonly'

    def serialisation_selection(self):
        """
        Creates drop down menu to select serialisation method.
        Methods: json, binary, xml.
        """

        # label2 ("Please select the serialisation method"
        serialisation_label = ttk.Label(self.frame2, text="Select serialisation method:")
        serialisation_label.pack(padx=10, pady=5, anchor='center')

        # create a combobox
        selected_method = tk.StringVar()
        serialisation_method = ttk.Combobox(self.frame2, textvariable=selected_method)

        serialisation_method['values'] = ["XML", "Binary", "Json"]

        # prevent typing a value
        serialisation_method['state'] = 'readonly'

        # place the widget
        serialisation_method.config(width=10)
        serialisation_method.pack(padx=10, pady=10, anchor='center')

    def obj_selection(self):
        """
        Creates drop down menu to select from sample objects.
        Object types: dictionaries, lists
        """

        # label2 ("Please select the serialisation method"
        obj_selection_label = ttk.Label(self.sub_frame, text="Select object:")
        obj_selection_label.pack(padx=10, pady=5, side=LEFT)

        # create a combobox
        selected_object = tk.StringVar()
        selection_obj = ttk.Combobox(self.sub_frame, textvariable=selected_object)

        selection_obj['values'] = ["Dictionary 1", "Dictionary 2"]

        # prevent typing a value
        selection_obj['state'] = 'readonly'

        # place the widget
        selection_obj.config(width=10)
        selection_obj.pack( padx=10, pady=5, side= LEFT)


    def encryption_option(self):
        """
        Creates tick box to select encryption method.
        Encryption options - Yes, No.
        """

        encryption_label = ttk.Label(self.frame3, text="Encrypt file:")
        encryption_label.pack( padx=10, pady=5, side= TOP)

        radio_var = tk.StringVar()
        # Checkbutton(self.frame3, text="Yes", variable=var_yes).pack( padx=10, pady=5,side= TOP)

        # Checkbutton(self.frame3, text="No", variable=var_no).pack( padx=10, pady=5,side= TOP)
        sub_frame=tk.Frame(self.frame3)
        c1 = tk.Radiobutton(sub_frame, text='Yes', value='Yes', variable=radio_var,tristatevalue=" ")
        c2 = tk.Radiobutton(sub_frame, text='No', value='No', variable=radio_var,tristatevalue=" ")
        c1.pack(fill='x', padx=10, pady=5, side=LEFT)
        c2.pack(fill='x', padx=10, pady=5,side=LEFT)
        sub_frame.pack(anchor=CENTER)

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

        execute_button = tk.Button(self.frame4, text="Upload", command=file_transfer_callback)
        execute_button.config(width=10)
        execute_button.pack(padx=10, pady=10)

    def text_box_func(self):

        # Create text widget and specify size.
        self.T = Text(self.frame5)
        self.T.pack()

UserInterface()
