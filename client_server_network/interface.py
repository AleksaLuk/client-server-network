"""
User interface
"""

from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import *
from tkinter.filedialog import askopenfile
from client import transfer_file
import tkinter as tk


class UserInterface:
    def __init__(self):

        # config the root window and frames
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title('Data Processing')
        self.set_geometry()
        self.outer_frame = tk.Frame(self.root, highlightbackground="white", highlightthickness=1)
        self.outer_frame.pack(padx=5, pady=5,expand=False)
        self.frame1 = tk.Frame(self.outer_frame, highlightbackground="white", highlightthickness=1)
        self.frame1.pack(side=tk.TOP, fill=BOTH, expand=False)
        self.sub_frame1 = tk.Frame(self.frame1)
        self.sub_frame1.pack(padx=5,pady=5,anchor=CENTER)
        self.frame2 = tk.Frame(self.outer_frame, highlightbackground="white", highlightthickness=1)
        self.frame2.pack(side=tk.TOP, fill=BOTH, expand=False)
        self.sub_frame2 = tk.Frame(self.frame2)
        self.sub_frame2.pack(padx=5,pady=5,anchor=CENTER)
        self.frame3 = tk.Frame(self.outer_frame, highlightbackground="white", highlightthickness=1)
        self.frame3.pack(side=tk.TOP, fill=BOTH, expand=False)
        self.sub_frame3 = tk.Frame(self.frame3)
        self.sub_frame3.pack(padx=5,pady=5,anchor=CENTER)
        self.frame4 = tk.Frame(self.outer_frame, highlightbackground="white", highlightthickness=1)
        self.frame4.pack(side=tk.TOP, fill=BOTH, expand=False)
        self.sub_frame4 = tk.Frame(self.frame4)
        self.sub_frame4.pack(padx=5,pady=5,anchor=CENTER)
        self.frame5 = tk.Frame(self.outer_frame, highlightbackground="white", highlightthickness=1)
        self.frame5.pack(side=tk.TOP, fill=BOTH, expand=False)
        self.frame6 = tk.Frame(self.outer_frame, highlightbackground="white", highlightthickness=1)
        self.frame6.pack(side=tk.TOP, fill=BOTH, expand=False)
        self.sub_frame6 = tk.Frame(self.frame6)
        self.sub_frame6.pack(padx=5,pady=5,anchor=E)
        self.browse_file()
        self.obj_selection()
        self.serialisation_selection()
        self.encryption_option()
        self.execute_button()
        self.text_box()
        self.info_exit()
        self.selections = {}
        self.root.mainloop()

    def set_geometry(self):
        """
        Calculates geometry to center the window.

        """

        window_height = 670
        window_width = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    def browse_file(self):
        """
        Creates button to upload files.
        """

        file_select = ttk.Label(self.sub_frame1, text="Select file or object for transfer:")
        file_select.pack(pady=5)

        # Text for file select label
        file_select_label = ttk.Label(self.sub_frame1, text="Select file:")
        file_select_label.pack(padx=10,pady=5,side=LEFT)

        # create a combobox
        selected_file = tk.StringVar()
        file_path = ttk.Combobox(self.sub_frame1, textvariable=selected_file)

        def select_file_callback():
            """
            Selects file path
            """

            # file path setup
            file_path = askopenfile(mode='r', filetypes=[('text files', '.txt')])
            if file_path is not None:
                pass
            self.file_path = file_path.name
            self.T.insert("1.0",f"1) File Path selected: {self.file_path}\n")

        # create a button
        file_path_button = tk.Button(self.sub_frame1, text='Browse',command=select_file_callback)
        file_path_button.config(width=10)
        file_path_button.pack( pady=5, side=LEFT)

        # prevent typing a value
        file_path['state'] = 'readonly'

    def serialisation_selection(self):
        """
        Creates drop down menu to select serialisation method.
        Methods: json, binary, xml.
        """

        # Text for serialisation method label
        serialisation_label = ttk.Label(self.sub_frame2, text="Select object serialisation method:")
        serialisation_label.pack(pady=5)

        # create a combobox
        def serialisation_callback(event):
            self.T.insert(END, f"3) Method selected: {selected_method.get()}\n")
        selected_method = tk.StringVar()
        serialisation_method = ttk.Combobox(self.sub_frame2, textvariable=selected_method)
        serialisation_method.bind("<<ComboboxSelected>>", serialisation_callback)

        serialisation_method['values'] = ["XML", "Binary", "Json"]

        # prevent typing a value
        serialisation_method['state'] = 'readonly'

        # place the widget
        serialisation_method.config(width=10)
        serialisation_method.pack(pady=5)

    def obj_selection(self):
        """
        Creates drop down menu to select from sample objects.
        Object types: dictionaries, lists
        """

        # Text for select object label
        obj_selection_label = ttk.Label(self.sub_frame1, text="Select object:")
        obj_selection_label.pack(padx=10, pady=5, side=LEFT)

        # create a combobox
        def obj_selection_callback(event):
            self.T.insert(END, f"2) Object selected: {selected_object.get()}\n")
        selected_object = tk.StringVar()
        selection_obj = ttk.Combobox(self.sub_frame1, textvariable=selected_object)
        selection_obj.bind("<<ComboboxSelected>>", obj_selection_callback)

        selection_obj['values'] = ["Dictionary 1", "Dictionary 2"]

        # prevent typing a value
        selection_obj['state'] = 'readonly'

        # place the widget
        selection_obj.config(width=10)
        selection_obj.pack(pady=5, side=LEFT)

    def encryption_option(self):
        """
        Creates tick box to select encryption method.
        Encryption options - Yes, No.
        """

        # Text for encrypt file label
        encryption_label = ttk.Label(self.sub_frame3, text="Encrypt file/object:")
        encryption_label.pack(pady=5, side=TOP)

        # create a radio button
        def encryption_callback():
            self.T.insert(END, f"4) Encryption: {radio_var.get()}\n")
        radio_var = tk.StringVar()
        c1 = tk.Radiobutton(self.sub_frame3, text='Yes', value='Yes', variable=radio_var, tristatevalue=" ", command=encryption_callback)
        c2 = tk.Radiobutton(self.sub_frame3, text='No', value='No', variable=radio_var, tristatevalue=" ", command=encryption_callback)

        # place the widget
        c1.pack(pady=5, side=LEFT)
        c2.pack(pady=5,side=LEFT)

    def execute_button(self):
        """
        Executes operation.
        """

        def file_transfer_callback():
            """
            Show file transfer status information.

            """
            showinfo(
                title='Information',
                message='File transfer initiated'
            )
            transfer_file("0.0.0.0", 5006, self.file_path)
            self.T.insert(END, "5) Operation status: File transfer initiated\n")

        # create a button
        execute_button = tk.Button(self.sub_frame4, text="Upload", command=file_transfer_callback)

        # place the widget
        execute_button.config(width=10)
        execute_button.pack(pady=5)

    def text_box(self):
        """
        Message box with status information.

        """

        # Create a text widget
        self.T = Text(self.frame5)

        # place the widget
        self.T.pack()

    def info_exit(self):
        """
        Creates information and exit buttons.
        """
        def info_button_callback():
            """
            Show process information.

            """
            showinfo(
                title='Information',
                message='To select file for transfer user is required to:\n'
                        '1) Click Browse button to select file \n'
                        '2) Select from encryption options - Yes/No \n'
                        '3) Click the Upload button to initialise transfer \n'

            )

        # create a button
        info_button = tk.Button(self.sub_frame6, text="Info", command=info_button_callback)
        exit_button = tk.Button(self.sub_frame6, text="Exit", command=self.root.destroy)
        info_button.pack(side=LEFT, pady=5)
        exit_button.pack(side=LEFT, pady=5)

UserInterface()
