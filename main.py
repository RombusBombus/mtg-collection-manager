import tkinter as tk
from pages.SearchPage import SearchPage
import ttkbootstrap as ttkbs


class App(ttkbs.tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Collection Manager")
        self.geometry("1000x800")
        style = ttkbs.Style("darkly")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        navbar = tk.Frame(self, bg="lightgrey", height=50)
        navbar.grid(row=0, column=0, sticky="ew")
        navbar.grid_columnconfigure(0, weight=1)

        self.container = tk.Frame(self)
        self.container.grid(row=1, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}

        for Page in all_pages:
            page = Page(parent=self.container, controller=self)
            self.pages[Page.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        tk.Button(
            navbar, text="Search", command=lambda: self.show_page("SearchPage")
        ).grid(row=0, column=0, sticky='nsew')

        self.show_page("SearchPage")

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()


all_pages = [SearchPage]

if __name__ == "__main__":
    app = App()
    app.mainloop()
