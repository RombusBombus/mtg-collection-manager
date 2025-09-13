import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os

# File to store collection
COLLECTION_FILE = "mtg_collection.csv"

# Load collection if file exists
def load_collection():
    if not os.path.exists(COLLECTION_FILE):
        return []
    with open(COLLECTION_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

# Save collection to file
def save_collection():
    with open(COLLECTION_FILE, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Name', 'Set', 'Quantity', 'Condition']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for card in collection:
            writer.writerow(card)

# Add a new card
def add_card():
    name = name_entry.get()
    set_name = set_entry.get()
    qty = qty_entry.get()
    condition = condition_entry.get()

    if not name or not set_name or not qty:
        messagebox.showwarning("Input Error", "Please fill all fields")
        return
    
    try:
        qty = int(qty)
    except ValueError:
        messagebox.showwarning("Input Error", "Quantity must be a number")
        return

    card = {'Name': name, 'Set': set_name, 'Quantity': qty, 'Condition': condition}
    collection.append(card)
    update_tree()
    save_collection()
    clear_entries()

# Update selected card
def update_card():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Card", "Please select a card to update")
        return
    index = int(selected[0])
    collection[index] = {
        'Name': name_entry.get(),
        'Set': set_entry.get(),
        'Quantity': int(qty_entry.get()),
        'Condition': condition_entry.get()
    }
    update_tree()
    save_collection()
    clear_entries()

# Delete selected card
def delete_card():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Card", "Please select a card to delete")
        return
    index = int(selected[0])
    collection.pop(index)
    update_tree()
    save_collection()
    clear_entries()

# Clear entry fields
def clear_entries():
    name_entry.delete(0, tk.END)
    set_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    condition_entry.delete(0, tk.END)

# Populate treeview
def update_tree():
    for i in tree.get_children():
        tree.delete(i)
    for idx, card in enumerate(collection):
        tree.insert("", "end", iid=idx, values=(card['Name'], card['Set'], card['Quantity'], card['Condition']))

# GUI Setup
root = tk.Tk()
root.title("MTG Collection Tracker")
root.geometry("600x400")

collection = load_collection()

# Entry fields
tk.Label(root, text="Name").grid(row=0, column=0, padx=5, pady=5)
tk.Label(root, text="Set").grid(row=1, column=0, padx=5, pady=5)
tk.Label(root, text="Quantity").grid(row=2, column=0, padx=5, pady=5)
tk.Label(root, text="Condition").grid(row=3, column=0, padx=5, pady=5)

name_entry = tk.Entry(root)
set_entry = tk.Entry(root)
qty_entry = tk.Entry(root)
condition_entry = tk.Entry(root)

name_entry.grid(row=0, column=1, padx=5, pady=5)
set_entry.grid(row=1, column=1, padx=5, pady=5)
qty_entry.grid(row=2, column=1, padx=5, pady=5)
condition_entry.grid(row=3, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Add Card", command=add_card).grid(row=4, column=0, padx=5, pady=5)
tk.Button(root, text="Update Card", command=update_card).grid(row=4, column=1, padx=5, pady=5)
tk.Button(root, text="Delete Card", command=delete_card).grid(row=4, column=2, padx=5, pady=5)
tk.Button(root, text="Clear Fields", command=clear_entries).grid(row=4, column=3, padx=5, pady=5)

# Treeview for displaying collection
columns = ("Name", "Set", "Quantity", "Condition")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=5, column=0, columnspan=4, sticky='nsew')

# Scrollbar
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=5, column=4, sticky='ns')

update_tree()
root.mainloop()
