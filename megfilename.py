#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import os


class GUI:
    def __init__(self, master, dpbox1, dpbox2, dpbox3, pat):

        self.master = master
        master.title("String Generator")
        self.initialize_variables(master, dpbox1, dpbox2, dpbox3, pat)
        self.format_layout(master)
    # functions/methods

        #initializes objects and variables
    def initialize_variables(self, master, dpbox1, dpbox2, dpbox3, pat):
        self.mainframe = ttk.Frame(master, padding=(20, 20, 20, 20))
        self.name = self.read_file2(pat).split("/")[1]
        self.name = self.name.strip()

        self.initials = self.name.split()
        try:
            self.initials = self.initials[0][0] + self.initials[len(self.initials) - 1][0]
            self.initials = self.initials.lower()
        except:
            print("Name does not have at least 2 words")
            self.initials = self.initials[0][0]
            self.initials = self.initials.lower()
        self.name_label = ttk.Label(self.mainframe, text="Patient Name: " + self.name)
        self.num_menu_var = StringVar()
        self.num_menu_var2 = StringVar()
        self.current_index = [0]
        self.num_menu_var.set("Current Index: 0")
        self.num_label = ttk.Label(self.mainframe, textvariable=self.num_menu_var)
        self.loc_label = ttk.Label(self.mainframe, text="Location: ")
        self.eeg_meg_label = ttk.Label(self.mainframe, text="No_EEG/MEG")
        self.first_menu_var = StringVar()
        self.first_menu_list = self.read_file(dpbox1)
        self.first_menu_var.set(self.first_menu_list[0])
        self.first_menu = OptionMenu(self.mainframe, self.first_menu_var, *self.first_menu_list)
        try:
            self.num_limit = int(os.environ['MEGFILENAME_MAX_INDEX'])
            self.num_menu_list = list(range(1, self.num_limit + 1))
        except:
            self.num_menu_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.num_menu_list = ['Autopick'] + self.num_menu_list
        self.num_menu_var2.set(self.num_menu_list[0])
        self.num_menu = OptionMenu(self.mainframe, self.num_menu_var2, *self.num_menu_list)
        self.user_text = StringVar()
        self.user_text.set(self.initials)
        self.user_entry = ttk.Entry(self.mainframe, textvariable=self.user_text)
        self.loc_menu_var = StringVar()
        self.loc_menu_list = self.read_file(dpbox2)
        self.loc_menu_var.set(self.loc_menu_list[0])
        self.loc_menu = OptionMenu(self.mainframe, self.loc_menu_var, *self.loc_menu_list)
        self.eeg_meg_var = StringVar()
        self.eeg_meg_list = self.read_file(dpbox3)
        self.eeg_meg_var.set(self.eeg_meg_list[0])
        self.eeg_meg_menu = OptionMenu(self.mainframe, self.eeg_meg_var, *self.eeg_meg_list)
        self.protocol_var = StringVar()
        self.protocol_list = ["Choose Protocol", "Functional Meg"]
        self.protocol_var.set(self.protocol_list[0])
        self.protocol_menu = OptionMenu(self.mainframe, self.protocol_var, *self.protocol_list)
        self.exec_protocol_button = ttk.Button(self.mainframe, text="Start Protocol", command=self.protocol)
        self.reset_button = ttk.Button(self.mainframe, text='Reset',
                                       command=lambda: self.reset(self.first_menu_var, self.num_menu_var2,
                                                                  self.user_text, self.loc_menu_var,
                                                                  self.eeg_meg_var, self.output1_text,
                                                                  self.output2_text, self.first_menu_list,
                                                                  self.num_menu_list, self.loc_menu_list,
                                                                  self.eeg_meg_list))
        self.combine_button = ttk.Button(self.mainframe, text='New String',
                                         command=lambda: self.combine(self.first_menu_var, self.num_menu_var,
                                                                      self.num_menu_var2, self.user_text,
                                                                      self.loc_menu_var,
                                                                      self.eeg_meg_var, self.output1_text,
                                                                      self.output2_text, self.current_index))
        self.combine_button.bind("<Button-1>", self.callback)
        self.exit_button = ttk.Button(self.mainframe, text='Exit', command=lambda: self.exit_func(master))
        self.output1_label = ttk.Label(self.mainframe, text='SEF/MEF File String: ')
        self.output1_text = Text(self.mainframe, width=60, height=2, font=("Times New Roman", 16))
        self.output2_label = ttk.Label(self.mainframe, text='RAW File String: ')
        self.output2_text = Text(self.mainframe, width=60, height=2, font=("Times New Roman", 16))
        self.output3_label = ttk.Label(self.mainframe, text='Additional Comments: ')
        self.output3_text = Text(self.mainframe, width=60, height=2, font=("Times New Roman", 16))

        #configures the layout(spacing, placement, size, etc.)
    def format_layout(self, master):
        self.master.columnconfigure(1, weight=1)
        self.master.rowconfigure(1, weight=1)
        self.mainframe.grid(row=1, column=1, sticky=(N, E, S, W))
        self.mainframe.columnconfigure(1, weight=1, minsize=80)  # code for each column and row of mainframe to expand
        self.mainframe.columnconfigure(2, weight=1, minsize=80)
        self.mainframe.columnconfigure(3, weight=1, minsize=80)
        self.mainframe.columnconfigure(4, weight=1, minsize=80)
        self.mainframe.columnconfigure(5, weight=1, minsize=80)
        self.mainframe.rowconfigure(1, weight=1, minsize=25)
        self.mainframe.rowconfigure(2, weight=1, minsize=25)
        self.mainframe.rowconfigure(3, weight=1, minsize=25)
        self.mainframe.rowconfigure(4, weight=1, minsize=25)
        self.mainframe.rowconfigure(5, weight=1, minsize=25)
        self.mainframe.rowconfigure(6, weight=1, minsize=25)
        self.name_label.grid(row=1, column=1, sticky=(N, E, S, W), padx=10, pady=5)
        self.num_label.grid(row=2, column=2, sticky=(N, S), padx=10, pady=5)
        self.loc_label.grid(row=2, column=4, sticky=(N, S))
        self.eeg_meg_label.grid(row=2, column=5, sticky=(N, S), padx=10, pady=5)
        self.first_menu.grid(row=3, column=1, sticky=(N, E, S, W), padx=10, pady=15)
        self.num_menu.grid(row=3, column=2, sticky=(N, E, S, W), padx=10, pady=15)
        self.user_entry.grid(row=3, column=3, sticky=(N, E, S, W), padx=10, pady=15)
        self.loc_menu.grid(row=3, column=4, sticky=(N, E, S, W), padx=10, pady=15)
        self.eeg_meg_menu.grid(row=3, column=5, sticky=(N, E, S, W), padx=10, pady=15)
        self.protocol_menu.grid(row=4, column=1, sticky=(N, E, S, W), padx=10, pady=15)
        self.exec_protocol_button.grid(row=4, column=2, sticky=(N, E, S, W), padx=10, pady=15)
        self.reset_button.grid(row=4, column=4, sticky=(N, E, S, W), padx=10, pady=15)
        self.combine_button.grid(row=4, column=3, sticky=(N, E, S, W), padx=10, pady=15)
        self.exit_button.grid(row=4, column=5, sticky=(N, E, S, W), padx=10, pady=15)
        self.output1_label.grid(row=5, column=1, sticky=(N, W, S), padx=10, pady=15)
        self.output1_text.grid(row=5, column=2, columnspan=4, sticky=(N, E, S, W), pady=15)
        self.output2_label.grid(row=6, column=1, sticky=(N, W, S), padx=10, pady=15)
        self.output2_text.grid(row=6, column=2, columnspan=4, sticky=(N, E, S, W), pady=15)
        self.output3_label.grid(row=7, column=1, sticky=(N, W, S), padx=10, pady=15)
        self.output3_text.grid(row=7, column=2, columnspan=4, sticky=(N, E, S, W), pady=15)



    def callback(self, event):
        self.update_label(self.num_menu_var, self.num_menu_var2, self.current_index)

        # returns a list of the words in the text file
    def read_file(self, path):
        f = open(path, "r")
        return f.read().split()

    def read_file2(self, path):
        f = open(path, "r")
        return f.read()

    def exit_func(self, root):
        root.destroy()

        # executes before combine
    def update_label(self, tkvar, tkvar2, current_index):
        prefix = "Current Index: "
        if tkvar2.get() != "Autopick":
            if (current_index[0] == int(tkvar2.get())):
                current_index[0] = current_index[0] + 1
                tkvar2.set(current_index[0])
            else:
                current_index[0] = int(tkvar2.get())
        else:
            current_index[0] = current_index[0] + 1
        tkvar.set(prefix + str(current_index[0]))

    def combine(self, dbv1, dbv2_1, dbv2, entryvar, dbv3, dbv4, text1, text2, current_index):
        text1.delete(1.0, END)  # since text is multi-line, 1.0 means line 1, char 0
        text2.delete(1.0, END)
        list_strings = [dbv1.get(), dbv2.get(), entryvar.get(), dbv3.get(), dbv4.get()]
        for i in range(len(list_strings) - 1, -1, -1):
            if list_strings[i] in ["NULL", ""]:
                del list_strings[i]
        for j in range(len(list_strings)):
            if list_strings[j] in ['Autopick']:
                list_strings[j] = str(current_index[0])
        if (dbv1.get() in ["SEF", "MEF"]):
            text1.insert(1.0, "_".join(list_strings) + "_avg")
        text2.insert(1.0, "_".join(list_strings) + "_raw")

    def reset(self, dbv1, dbv2, entryv, dbv3, dbv4, text1, text2, dbv1_list, dbv2_list, dbv3_list, dbv4_list):
        dbv1.set(dbv1_list[0])
        dbv2.set(dbv2_list[0])
        dbv3.set(dbv3_list[0])
        dbv4.set(dbv4_list[0])
        entryv.set(self.initials)
        text1.delete(1.0, END)
        text2.delete(1.0, END)
        self.current_index = [0]
        self.num_menu_var.set("Current Index: 0")
        # reset the protocol menu
        self.protocol_var.set(self.protocol_list[0])
        # reset the protocol button command
        self.exec_protocol_button.configure(text="Start Protocol", command=self.protocol)
        # reset the extra comments
        self.output3_text.delete(1.0, END)

    # allows for future protocols to be added and edited.
    def protocol(self):
        if (self.protocol_var.get() == "Choose Protocol"):
            pass
        elif (self.protocol_var.get() == "Functional Meg"):
            self.output1_text.delete(1.0, END)
            self.output2_text.delete(1.0, END)
            self.output3_text.delete(1.0, END)
            f = open("mfn-funcmegprotocol.txt")
            lines = f.read().split("\n")
            f.close()
            self.output3_text.delete(1.0, END)
            self.output3_text.insert(1.0, "Functional Meg selected. Press \"Next Protocol Step\"")
            self.exec_protocol_button.configure(text="Next Protocol Step", command=lambda: self.functional_meg(lines))

    def functional_meg(self, lines):
        try:
            curr_line = lines.pop(0)
        except:
            self.reset(self.first_menu_var, self.num_menu_var2, self.user_text, self.loc_menu_var,
                       self.eeg_meg_var, self.output1_text, self.output2_text, self.first_menu_list,
                       self.num_menu_list, self.loc_menu_list, self.eeg_meg_list)
            return
        curr_line = curr_line.split("/")
        for i in range(len(curr_line) - 1, -1, -1):
            curr_line[i] = curr_line[i].strip()
        to_process = curr_line[0]
        to_process = to_process.split("_")
        for i in range(len(to_process) - 1, -1, -1):
            to_process[i] = to_process[i].strip()
        curr_line[0] = self.add_initials(to_process)
        self.output2_text.delete(1.0, END)
        self.output3_text.delete(1.0, END)
        self.output2_text.insert(1.0, curr_line[0])
        if (len(curr_line) == 2):
            self.output3_text.insert(1.0, curr_line[1])

    def add_initials(self, mylist):
        x = iter(mylist)
        # returns the value of the number in the list, and then gives the index of that number
        try:
            number = next(string for string in x if string.isdigit())
        except StopIteration:  # reached last line of protocol, curr_line[0] should be empty string
            return ""
        index = mylist.index(number)
        mylist.insert(index + 1, self.initials)
        return "_".join(mylist)


dpbox1_fname = "mfn-dropdownbox1.txt"
dpbox2_fname = "mfn-dropdownbox2.txt"
dpbox3_fname = "mfn-dropdownbox3.txt"
pat_fname = "mfn-myNames.txt"
root = Tk()
my_gui = GUI(root, dpbox1_fname, dpbox2_fname, dpbox3_fname, pat_fname)
root.mainloop()
