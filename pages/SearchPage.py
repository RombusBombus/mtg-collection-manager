import tkinter as tk
from tkinter import ttk
from ScryfallApi import get_all_prints
import requests
from PIL import Image, ImageTk
from io import BytesIO
import os
from pathlib import Path
import pandas as pd


image_size = 'normal'
collection_file = 'collection.csv'


class SearchPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.search_entry = tk.Entry(self, width=40)
        self.search_entry.grid(row=0, column=0, sticky='ew')
        self.search_entry.bind('<Return>', lambda event: self.search())

        self.tags_entry = tk.Entry(self, width=40)
        self.tags_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.tags_entry.bind('<Return>', lambda event: self.search())

        search_button = tk.Button(self, text="Search", command=self.search)
        search_button.grid(row=0, column=2, padx=10, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        columns = ('Print', 'Released')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='w')

        self.tree.grid(row=1, column=0, columnspan=3, sticky='nsew')
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.tree.bind('<Return>', self.tree_enter)

        self.tk_image = ImageTk.PhotoImage(Image.open('default.png'))
        self.image_label = tk.Label(self, image=self.tk_image)
        self.image_label.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    def search(self):
        query = self.search_entry.get()
        self.data = get_all_prints(query)

        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for name, row in self.data.iterrows():
            _print = f'{row["set_name"]} ({row["set"].upper()}) - {row["collector_number"]}'
            self.tree.insert('', 'end', text=name, values=(_print, row['released_at']))

    def on_tree_select(self, event):
        selected_item = self.tree.focus()
        name = self.tree.item(selected_item, 'text')
        image_url = self.data.loc[name]['image_uris'][image_size]
        self.update_image(image_url)

    def tree_enter(self, event):
        selected_item = self.tree.focus()
        name = self.tree.item(selected_item, 'text')
        tags = self.tags_entry.get()

        id = self.data.loc[name, 'id']
        files = os.listdir(Path('./'))

        if collection_file not in files:
            pd.DataFrame({
                'card': [id],
                'number': [1],
                'tags': [tags]
            }).to_csv(collection_file, index=False)
        else:
            collection_data = pd.read_csv(collection_file)
            card_search = collection_data.loc[collection_data['card'] == id]
            if len(card_search) == 0:
                new_row = pd.DataFrame({
                    'card': [id],
                    'number': [1],
                    'tags': [tags]
                })
                collection_data = pd.concat([collection_data, new_row], ignore_index=True)
            else:
                idx = card_search.index[0]
                collection_data.loc[idx, 'number'] += 1
            
            collection_data.to_csv(collection_file, index=False)

    def update_image(self, url):
        response = requests.get(url)
        img_data = response.content
        image = Image.open(BytesIO(img_data))
        self.tk_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.tk_image)