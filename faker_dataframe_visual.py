#python script to generate random data and generate tkinter data frame

import tkinter as tk
from tkinter import ttk
import pandas as pd
from faker import Faker

class FakerDataFrame:
    #Generate random data
    def __init__(self, master):
        self.master = master
        self.master.title("Faker Dataframe Generator")
        self.master.geometry("1500x1000")

        #Initialize Faker as fake
        self.fake = Faker()
 
        #GUI components
        self.make_widgets()

    #Make the Treeview Widget
    def make_widgets(self):
        #Label and Entry for the Number of Records
        self.label = tk.Label(self.master, text="Number of Records:")
        self.label.pack(pady=10)
        
        self.table_entry = tk.Entry(self.master)
        self.table_entry.pack(pady=5)

        #Make Button
        self.make_button = tk.Button(self.master, text="Generate Faker Data", command=self.faker_gen_data)
        self.make_button.pack(pady=10)

        #Sort Button
        self.sorting_button = tk.Button(self.master, text="Sort Name", command=self.name_sort)
        self.sorting_button.pack(pady=10)

        #Insert data into the Treeview
        self.tree = ttk.Treeview(self.master)
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

    #Generate data
    def faker_gen_data(self):
        size = int(self.table_entry.get())

        table_field = {
            'Name': [self.fake.first_name()+" "+self.fake.last_name() for _ in range(size)],
            'Email': [self.fake.email() for _ in range(size)],
            'Address': [self.fake.address().replace('\n', ', ') for _ in range(size)], #Show address on singleline
            'Phone': [self.fake.phone_number() for _ in range(size)],
            'Job': [self.fake.job() for _ in range(size)]
        }
 
        #Make DataFrame
        self.df = pd.DataFrame(table_field)

        #Display data method to get functionality
        self.display_data(self.df)

    def display_data(self, df):
        #Clear data
        self.clear_tree()

        #Setup columns for Treeview
        self.tree["column"] = list(df.columns)
        self.tree["show"] = "headings"

        #Add adjust_width_columns to dynamically adjust column width to data
        self.adjust_width_columns(df)

        #Insert data to Treeview
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=list(row))

    #Clear tree data
    def clear_tree(self):
        self.tree.delete(*self.tree.get_children())

    #Allow column width adjustment for data length
    def adjust_width_columns(self, df):
        for length in df.columns:
            max_length = max([len(str(value)) for value in df[length]] + [len(length)])
            self.tree.column(length, width=max_length*10) #scale width by 10 factor
            self.tree.heading(length, text=length)

    #Sort names alphabetically method
    def name_sort(self):
        #Replace the name column in df with sorted values
        self.df = self.df.sort_values(by=['Name'])
        #Call display data to print out the df values to Tkinter GUI
        self.display_data(self.df)  

if __name__ == "__main__":
    #Run loop for GUI to get input and create dataframe
    root = tk.Tk()
    app = FakerDataFrame(root)
    root.mainloop()