import os
import tkinter as tk

from PIL import ImageTk, Image


class TestView(tk.Frame):
    def __init__(self, root: tk.Tk, event_channel):
        self.root = root
        self.root.update()
        self.height = self.root.winfo_height()
        self.width = self.root.winfo_width()
        tk.Frame.__init__(self, root, width=self.width, height=self.height)
        image_open = Image.open(os.getcwd() + "/assets/background.jpg")
        self.background_image = ImageTk.PhotoImage(image_open)
        self.background = tk.Label(self, image=self.background_image)
        self.background.pack(fill=tk.BOTH, expand=tk.YES)



