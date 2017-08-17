#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
import os


class GUI:
    def __init__(self, master, dpbox1, dpbox2, dpbox3, pat):

        self.master = master
        self.master.title("String Generator")
        self.initialize_variables(dpbox1, dpbox2, dpbox3, pat)
        self.format_layout()

    #initializes objects and variables
    def initialize_variables(self, dpbox1, dpbox2, dpbox3, pat):
        self.mainframe = ttk.Frame(self.master, padding=(20, 20, 20, 20))
        #gets patient name, as file has format where name is the second element between forward slashes
        self.name = self.read_file(pat).split("/")[1]
        self.name = self.name.strip()
        #gets initials from name, if only one word as name, duplicates the first initial
        self.initials = self.name.split()
        try:
            self.initials = self.initials[0][0] + self.initials[len(self.initials) - 1][0]
            self.initials = self.initials.lower()
        except:
            print("Name does not have at least 2 words")
            self.initials = self.initials[0][0]
            self.initials = self.initials.lower()
        #initializes the menus, labels, and vars that are used in the menus
        self.name_label = ttk.Label(self.mainframe, text="Patient Name: " + self.name)
        self.num_menu_var = StringVar() #used as the variable to update the label
        self.num_menu_var2 = StringVar()    #used as the variable in the menu
        self.current_index = 0  #used to record the last used index to update the label
        self.num_menu_var.set("Current Index: 0")
        self.num_label = ttk.Label(self.mainframe, textvariable=self.num_menu_var)
        self.loc_label = ttk.Label(self.mainframe, text="Location: ")
        self.eeg_meg_label = ttk.Label(self.mainframe, text="No_EEG/MEG")
        self.first_menu_var = StringVar()
        self.first_menu_list = self.read_file(dpbox1).split()
        self.first_menu_var.set(self.first_menu_list[0])
        self.first_menu = OptionMenu(self.mainframe, self.first_menu_var, *self.first_menu_list)
        #reads from environment variable to set limit on max index in the list, otherwise uses 1-10
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
        self.loc_menu_list = self.read_file(dpbox2).split()
        self.loc_menu_var.set(self.loc_menu_list[0])
        self.loc_menu = OptionMenu(self.mainframe, self.loc_menu_var, *self.loc_menu_list)
        self.eeg_meg_var = StringVar()
        self.eeg_meg_list = self.read_file(dpbox3).split()
        self.eeg_meg_var.set(self.eeg_meg_list[0])
        self.eeg_meg_menu = OptionMenu(self.mainframe, self.eeg_meg_var, *self.eeg_meg_list)
        self.protocol_var = StringVar()
        self.protocol_list = ["Choose Protocol", "Functional Meg"]
        self.protocol_var.set(self.protocol_list[0])
        self.protocol_menu = OptionMenu(self.mainframe, self.protocol_var, *self.protocol_list)
        self.exit_button = ttk.Button(self.mainframe, text='Exit', command= self.exit_func)
        self.output1_label = ttk.Label(self.mainframe, text='SEF/MEF File String: ')
        self.output1_text = Text(self.mainframe, width=60, height=2, font=("Times New Roman", 16))
        self.output2_label = ttk.Label(self.mainframe, text='RAW File String: ')
        self.output2_text = Text(self.mainframe, width=60, height=2, font=("Times New Roman", 16))
        self.output3_label = ttk.Label(self.mainframe, text='Additional Comments: ')
        self.output3_text = Text(self.mainframe, width=60, height=2, font=("Times New Roman", 16))
        # initialize buttons
        self.exec_protocol_button = ttk.Button(self.mainframe, text="Start Protocol", command=self.protocol)
        self.reset_button = ttk.Button(self.mainframe, text='Reset', command = self.reset)
        self.combine_button = ttk.Button(self.mainframe, text='New String', command= self.combine)
        self.combine_button.bind("<Button-1>", self.callback_combine_button)

    #configures the layout(spacing, placement, size, etc.)
    def format_layout(self):
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

    #callback for combine_button, which updates the label
    def callback_combine_button(self, event):
        self.update_label()

    # returns the text in the text file
    def read_file(self, path):
        f = open(path, "r")
        return f.read()

    #allows exit button to exit program
    def exit_func(self):
        self.master.destroy()

    #updates the label that displays the current index, executes before combine
    def update_label(self):
        prefix = "Current Index: "
        #if autopick not selected, and current/last used index is the same as the selected one, automatically increase by 1
        if self.num_menu_var2.get() != "Autopick":
            if (self.current_index == int(self.num_menu_var2.get())):
                self.current_index = self.current_index + 1
                self.num_menu_var2.set(self.current_index)
            else: #if not the same, just update current index
                self.current_index = int(self.num_menu_var2.get())
        else:#if autopick selected, increase the index by one
            self.current_index = self.current_index + 1
        #update the variable that is used for the current index label
        self.num_menu_var.set(prefix + str(self.current_index))

    #function for combine button that concatenates the options chosen
    def combine(self):
        self.output1_text.delete(1.0, END)  # since text is multi-line, 1.0 means line 1, char 0
        self.output2_text.delete(1.0, END)
        #creates a list of all options selected
        list_strings = [self.first_menu_var.get(), self.num_menu_var2.get(), self.user_text.get(), self.loc_menu_var.get(), self.eeg_meg_var.get()]
        #removes an option if it is NULL
        for i in range(len(list_strings) - 1, -1, -1):
            if list_strings[i] in ["NULL", ""]:
                del list_strings[i]
        #if autopick is chosen for the index, make it new string choose
        for j in range(len(list_strings)):
            if list_strings[j] in ['Autopick']:
                list_strings[j] = str(self.current_index)
        #if first option is mef/sef, concatenate _avg instead of raw on the end.
        if (self.first_menu_var.get() in ["SEF", "MEF"]):
            self.output1_text.insert(1.0, "_".join(list_strings) + "_avg")
        self.output2_text.insert(1.0, "_".join(list_strings) + "_raw")

    #function for reset button, resets everything
    def reset(self):
        #reset the menus to the first item in the list
        self.first_menu_var.set(self.first_menu_list[0])
        self.num_menu_var2.set(self.num_menu_list[0])
        self.loc_menu_var.set(self.loc_menu_list[0])
        self.eeg_meg_var.set(self.eeg_meg_list[0])
        self.protocol_var.set(self.protocol_list[0])
        #reset the user text to the initials from the patient file
        self.user_text.set(self.initials)
        #reset the text outputs
        self.output1_text.delete(1.0, END)
        self.output2_text.delete(1.0, END)
        self.output3_text.delete(1.0, END)
        self.current_index = 0
        self.num_menu_var.set("Current Index: 0")
        # reset the protocol button command
        self.exec_protocol_button.configure(text="Start Protocol", command=self.protocol)

    # executes selected protocol when protocol button pressed, can add more protocols in self.protocol_list
    def protocol(self):
        if (self.protocol_var.get() == "Choose Protocol"):
            pass
        elif (self.protocol_var.get() == "Functional Meg"):
            self.output1_text.delete(1.0, END)
            self.output2_text.delete(1.0, END)
            self.output3_text.delete(1.0, END)
            #reads in from the protocol file, creates list of each line
            f = open("mfn-funcmegprotocol.txt")
            lines = f.read().split("\n")
            #removes blank/whitespace lines from protocol
            myiter = iter(lines)
            num_blank_lines = 0
            while True:
                try:
                    line = next(myiter)
                    if (line.strip() == ""):
                        num_blank_lines += 1
                except StopIteration:
                    break
            for i in range(0, num_blank_lines):
                lines.remove(line)
            f.close()
            self.output3_text.delete(1.0, END)
            self.output3_text.insert(1.0, "Functional Meg selected. Press \"Next Protocol Step\"")
            #binds protocol button to the function of the specific protocol. Will be reset in self.reset()
            self.exec_protocol_button.configure(text="Next Protocol Step", command=lambda: self.functional_meg(lines))

    #runs the functional meg protocol
    def functional_meg(self, lines):
        try:
            curr_line = lines.pop(0)
        except IndexError: #no lines left in protocol, so resets
            self.reset()
            return
        #text format is  displayed_protocol / comments
        curr_line = curr_line.split("/")
        for i in range(len(curr_line) - 1, -1, -1):
            curr_line[i] = curr_line[i].strip()
        to_process = curr_line[0]
        to_process = to_process.split("_")
        for i in range(len(to_process) - 1, -1, -1):
            to_process[i] = to_process[i].strip()
        #protocol includes all text except initials.
        curr_line[0] = self.add_initials(to_process)
        self.output1_text.delete(1.0, END)
        self.output2_text.delete(1.0, END)
        self.output3_text.delete(1.0, END)
        self.output2_text.insert(1.0, curr_line[0])
        #if there are comments, add them to textbox 3
        if (len(curr_line) == 2):
            self.output3_text.insert(1.0, curr_line[1])

    #addes initials in the functional meg protocol. Might be reusable if other protocols have same format.
    def add_initials(self, mylist):
        x = iter(mylist)
        # returns the value of the number in the list created from the protocol, and then gives the index of that number
        try:
            number = next(string for string in x if string.isdigit())
        except StopIteration:  # no number in protocol, so the protocol should be an empty string
            return ""
        index = mylist.index(number)
        #add the initials where they belong (after the number) and return rejoined string
        mylist.insert(index + 1, self.initials)
        return "_".join(mylist)

dpbox1_fname = "mfn-dropdownbox1.txt"
dpbox2_fname = "mfn-dropdownbox2.txt"
dpbox3_fname = "mfn-dropdownbox3.txt"
pat_fname = "mfn-myNames.txt"
root = Tk()
my_gui = GUI(root, dpbox1_fname, dpbox2_fname, dpbox3_fname, pat_fname)
root.mainloop()