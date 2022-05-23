"""
User interface
"""
import socket
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfile
import os
import configparser
from datetime import datetime, timedelta
from .client import Client
from .sample_files.sample_data import DATA


class UserInterface:
    """
    User interface for interacting with a server.

    Option 1: run with config file
    Option 2: run with tkinter GUI
    """

    def __init__(self, host: str = None, port: int = None):
        """
        :param host: The ip address or hostname of the server (do not pass if using config)
        :param port: The port of the server (do not pass if using config)
        """

        # Create client
        self.start_time = datetime.now()
        if host and port:
            self.client = Client(host, port)
            self.client.connection()

    def run(self, config_file=""):
        """
        Runs user interface, either by GUI or through configuration file

        :param config_file: path to config file (do not pass if not required)
        """

        if config_file:
            self._run_with_config(config_file)
        else:
            self._run_with_tkinter()

    @staticmethod
    def _run_with_config(config_file: str):
        """
        Runs connection through configuration file

        :param config_file: path to config file
        """

        config = configparser.ConfigParser()
        config.read(config_file)

        def send(client, config):
            if config["File"].getboolean("send"):
                file = config["File"]["filepath"].replace('"', "").replace("'", "")
                enc = config["File"].getboolean("encrypt")

                if not os.path.isfile(file):
                    print("Invalid file path")
                    return
                client.transfer_file(file, enc)

            if config["Object"].getboolean("send"):
                try:
                    obj = eval(config["Object"]["object"])
                except Exception as e:
                    print("[Object]object is not valid. Error:", e)
                    return
                enc = config["Object"].getboolean("encrypt")
                ser = config["Object"]["serialisation"]

                client.transfer_object(ser, obj, enc)

        if config["LocalServer"].getboolean("send"):
            host = config["LocalServer"]["host"]
            host = socket.gethostname() if host.lower() == "localhost" else host
            port = config["LocalServer"].getint("port")

            client = Client(host, port)
            client.connection()

            new_host = socket.gethostname()
            print(
                f"Could not connect to {config['LocalServer']['host']}, using {new_host} instead."
            )
            client = Client(new_host, port)
            client.connection()
            send(client, config)

        if config["AWS"].getboolean("send"):
            try:
                host = config["AWS"]["host"]
                port = int(config["AWS"]["port"])
                client = Client(host, port)
                client.connection()
                send(client, config)
            except OSError:
                print(f"Could not connect to {host}{port}")

    def _run_with_tkinter(self):
        """
        Runs connection using tkinter GUI
        """

        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Data Processing")
        self.set_geometry()
        self.outer_frame = tk.Frame(
            self.root, highlightbackground="white", highlightthickness=1
        )
        self.outer_frame.pack(padx=5, pady=5, expand=False)
        self.frame1 = tk.Frame(
            self.outer_frame, highlightbackground="white", highlightthickness=1
        )
        self.frame1.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        self.sub_frame1 = tk.Frame(self.frame1)
        self.sub_frame1.pack(padx=5, pady=5, anchor=tk.CENTER)
        self.frame2 = tk.Frame(
            self.outer_frame, highlightbackground="white", highlightthickness=1
        )
        self.frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        self.sub_frame2 = tk.Frame(self.frame2)
        self.sub_frame2.pack(padx=5, pady=5, anchor=tk.CENTER)
        self.frame3 = tk.Frame(
            self.outer_frame, highlightbackground="white", highlightthickness=1
        )
        self.frame3.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        self.sub_frame3 = tk.Frame(self.frame3)
        self.sub_frame3.pack(padx=5, pady=5, anchor=tk.CENTER)
        self.frame4 = tk.Frame(
            self.outer_frame, highlightbackground="white", highlightthickness=1
        )
        self.frame4.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        self.sub_frame4 = tk.Frame(self.frame4)
        self.sub_frame4.pack(padx=5, pady=5, anchor=tk.CENTER)
        self.frame5 = tk.Frame(
            self.outer_frame, highlightbackground="white", highlightthickness=1
        )
        self.frame5.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        self.frame6 = tk.Frame(
            self.outer_frame, highlightbackground="white", highlightthickness=1
        )
        self.frame6.pack(side=tk.TOP, fill=tk.BOTH, expand=False)
        self.sub_frame6 = tk.Frame(self.frame6)
        self.sub_frame6.pack(padx=5, pady=5, anchor=tk.E)
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
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        self.root.geometry(
            "{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate)
        )

    def browse_file(self):
        """
        Creates button to upload files.
        """

        file_select = ttk.Label(
            self.sub_frame1, text="Select file or object for transfer:"
        )
        file_select.pack(pady=5)

        # Text for file select label
        file_select_label = ttk.Label(self.sub_frame1, text="Select file:")
        file_select_label.pack(padx=10, pady=5, side=tk.LEFT)

        # create a combobox
        selected_file = tk.StringVar()
        file_path = ttk.Combobox(self.sub_frame1, textvariable=selected_file)

        def select_file_callback():
            """
            Selects file path
            """

            # file path setup
            file_path = askopenfile(
                mode="r",
                filetypes=[
                    ("text files", ".txt"),
                    ("pdf files", ".pdf"),
                    ("xml files", ".xml"),
                    ("picture files", ".jpg"),
                    ("picture files", ".jpeg"),
                ],
            )
            if file_path is not None:
                self.file_path = file_path.name
                self.selections["File path"] = self.file_path
                self.update_text_box()

        # create a button
        file_path_button = tk.Button(
            self.sub_frame1, text="Browse", command=select_file_callback
        )
        file_path_button.config(width=10)
        file_path_button.pack(pady=5, side=tk.LEFT)

        # prevent typing a value
        file_path["state"] = "readonly"

    def serialisation_selection(self):
        """
        Creates drop down menu to select serialisation method.
        Methods: json, binary.
        """

        # Text for serialisation method label
        serialisation_label = ttk.Label(
            self.sub_frame2, text="Select object serialisation method:"
        )
        serialisation_label.pack(pady=5)

        def serialisation_callback(event):
            self.selections["Serialisation method"] = selected_method.get()
            self.update_text_box()
            return event

        selected_method = tk.StringVar()

        # create a combobox
        serialisation_method = ttk.Combobox(
            self.sub_frame2, textvariable=selected_method
        )
        serialisation_method.bind("<<ComboboxSelected>>", serialisation_callback)

        serialisation_method["values"] = ["Binary", "Json"]

        # prevent typing a value
        serialisation_method["state"] = "readonly"

        # place the widget
        serialisation_method.config(width=10)
        serialisation_method.pack(pady=5)

    def obj_selection(self):
        """
        Creates drop down menu to select from sample objects.
        Object types: dictionaries, lists, classes (for binary serialisation only)
        """

        # Text for select object label
        obj_selection_label = ttk.Label(self.sub_frame1, text="Select object:")
        obj_selection_label.pack(padx=10, pady=5, side=tk.LEFT)

        def obj_selection_callback(event):
            self.selections["Selected object"] = selected_object.get()
            self.update_text_box()
            return event

        # create a combobox
        selected_object = tk.StringVar()
        selection_obj = ttk.Combobox(self.sub_frame1, textvariable=selected_object)
        selection_obj.bind("<<ComboboxSelected>>", obj_selection_callback)

        selection_obj["values"] = list(DATA.keys())

        # prevent typing a value
        selection_obj["state"] = "readonly"

        # place the widget
        selection_obj.config(width=10)
        selection_obj.pack(pady=5, side=tk.LEFT)

    def encryption_option(self):
        """
        Creates tick box to select encryption method.
        Encryption options - Yes, No.
        """

        # Text for encrypt file label
        encryption_label = ttk.Label(self.sub_frame3, text="Encrypt file/object:")
        encryption_label.pack(pady=5, side=tk.TOP)

        # create a radio button
        def encryption_callback():
            """
            Updates selection and UI console
            """

            self.selections["Encryption"] = radio_var.get()
            self.update_text_box()

        radio_var = tk.StringVar()
        enc1 = tk.Radiobutton(
            self.sub_frame3,
            text="Yes",
            value=True,
            variable=radio_var,
            tristatevalue=" ",
            command=encryption_callback,
        )
        enc2 = tk.Radiobutton(
            self.sub_frame3,
            text="No",
            value=False,
            variable=radio_var,
            tristatevalue=" ",
            command=encryption_callback,
        )

        # place the widget
        enc1.pack(pady=5, side=tk.LEFT)
        enc2.pack(pady=5, side=tk.LEFT)

    def execute_button(self):
        """
        Executes transfer operation.
        """

        def file_transfer_callback():
            """
            Show file transfer status information.
            """

            if "File path" not in self.selections:
                showinfo(
                    title="Error",
                    message="No file path given, please select using the browse button",
                )
            elif "Encryption" not in self.selections:
                showinfo(
                    title="Error",
                    message="Please select encryption (yes or no) for file transfer",
                )
            else:
                showinfo(title="Information", message="Transfer initiated")
                self.client.transfer_file(self.file_path, encrypt=self.selections["Encryption"])
                self.selections["file_transfer"] = "True"
                self.update_text_box()

                try:
                    for line in self.get_log_output():
                        self.log_box.insert(tk.END, line)
                except (tk.TclError, AttributeError):
                    self.log_popup()

        def object_transfer_callback():
            """
            Show file transfer status information.
            """

            if "Selected object" not in self.selections:
                showinfo(title="Error", message="Please an object for transfer")
            elif "Serialisation method" not in self.selections:
                showinfo(
                    title="Error",
                    message="Please select serialisation method for object transfer",
                )
            elif "Encryption" not in self.selections:
                showinfo(
                    title="Error",
                    message="Please select encryption (yes or no) for object transfer",
                )
            else:
                showinfo(title="Information", message="Transfer initiated")
                data = DATA[self.selections["Selected object"]]
                self.client.transfer_object(
                    self.selections["Serialisation method"], data, self.selections["Encryption"]
                )
                try:
                    for line in self.get_log_output():
                        self.log_box.insert(tk.END, line)
                except (tk.TclError, AttributeError):
                    self.log_popup()

        file_transfer_button = tk.Button(
            self.sub_frame4, text="Upload file", command=file_transfer_callback
        )
        object_transfer_button = tk.Button(
            self.sub_frame4, text="Upload object", command=object_transfer_callback
        )

        # place the widget
        file_transfer_button.config(width=10)
        file_transfer_button.pack(side=tk.LEFT, pady=5)
        object_transfer_button.config(width=10)
        object_transfer_button.pack(side=tk.LEFT, pady=5)

    def text_box(self):
        """
        Message box with status information.
        """

        # Create a text widget
        self.text = tk.Text(self.frame5)

        # place the widget
        self.text.pack()

    def info_exit(self):
        """
        Creates information and exit buttons.
        """

        def info_button_callback():
            """
            Show instructions.
            """

            showinfo(
                title="Information",
                message="To transfer file:\n"
                "1) Select file using browse button\n"
                "2) Select encryption option\n"
                "3) Click Upload button to initiate transfer\n\n"
                "To transfer object:\n"
                "1) Select object from dropdown\n"
                "2) Select serialisation option\n"
                "3) Select encryption option\n"
                "4) Click Upload button to initiate transfer\n",
            )

        # create a button
        info_button = tk.Button(
            self.sub_frame6, text="Info", command=info_button_callback
        )
        exit_button = tk.Button(self.sub_frame6, text="Exit", command=self.root.destroy)
        info_button.pack(side=tk.LEFT, pady=5)
        exit_button.pack(side=tk.LEFT, pady=5)

    def update_text_box(self):
        """
        Updates UI console with user selections
        """

        self.text.delete("1.0", tk.END)
        text = "\n".join([f"{key}: {val}" for key, val in self.selections.items()])
        self.text.insert("1.0", text)
        if "Selected object" in self.selections:
            self.text.insert(
                tk.END, f"\nData selected: {DATA[self.selections['Selected object']]}"
            )

    def log_popup(self):
        """
        Provides user with popup showing file transfer log history
        """

        top = tk.Toplevel()
        top.resizable(True, True)
        top.geometry("500x400")
        top.title("Log History")

        # Create a text widget
        self.log_box = tk.Text(top)

        # place the widget
        self.log_box.pack(expand=True, fill=tk.BOTH)

        for line in self.get_log_output():
            self.log_box.insert(tk.END, line)

    def get_log_output(self):
        """
        Gets log history from log file

        :yield: each log line (only from current session)
        """

        filepath = "client_history.log"
        with open(filepath, "r") as file:
            for line in file.readlines():
                line_time = datetime.strptime(line[8:27], "%Y-%m-%d %H:%M:%S")
                if line_time >= (self.start_time - timedelta(seconds=1)):
                    yield line
