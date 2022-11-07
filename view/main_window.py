import asyncio
import tkinter as tk

import settings
from view.qr_view import QRView


class Window:
    def __init__(self, loop, event_channel):
        self.loop = loop
        self.root = tk.Tk()
        self.event_channel = event_channel
        self.root.geometry(self.calculate_screen_size())
        self.root.configure(bg='#000')
        # self.root.wm_attributes('-type', 'splash')
        self._frame = None
        self.switch_frame(QRView)
        # self.root.attributes('-fullscreen', True)
        self.root.resizable(False, False)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self.root, self.event_channel)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def calculate_screen_size(self):
        if settings.FULLSCREEN:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            return str(screen_width) + 'x' + str(screen_height)
        else:
            return '400x400'

    async def show(self):
        while True:
            self.root.update()
            await asyncio.sleep(.1)
