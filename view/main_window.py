import asyncio
import tkinter as tk

import settings
from view.qr_view import QRView


class Window:
    def __init__(self, loop, event_channel):
        self.loop = loop
        self.root = tk.Tk()
        self.event_channel = event_channel
        self.set_screen_size()
        self.root.configure(bg='#000')
        self._frame = None
        self.switch_frame(QRView)
        self.root.resizable(False, False)

    def switch_frame(self, frame_class) -> None:
        new_frame = frame_class(self.root, self.event_channel)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def set_screen_size(self) -> None:
        if settings.FULLSCREEN:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            self.root.geometry(str(screen_width) + 'x' + str(screen_height))
            self.root.wm_attributes('-type', 'splash')
            self.root.attributes('-fullscreen', True)
        else:
            self.root.geometry('800x480')

    async def show(self) -> None:
        while True:
            self.root.update()
            await asyncio.sleep(.1)
